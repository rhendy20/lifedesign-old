import React, { useState, useEffect, useCallback, useRef } from "react";
import {
  Animated,
  Easing,
  FlatList,
  KeyboardAvoidingView,
  Platform,
  Pressable,
  StyleSheet,
  TextInput,
  TouchableOpacity,
  View,
  Text,
} from "react-native";
import { Audio } from "expo-av";
import * as Haptics from "expo-haptics";
import { LinearGradient } from "expo-linear-gradient";
import type { Reflection } from "shared";

const API_URL = process.env.EXPO_PUBLIC_API_URL ?? "http://localhost:3000";
const MAX_RECORDING_SECONDS = 5 * 60;
const WARNING_SECONDS = 4 * 60 + 30;
type ScreenMode = "capture" | "review" | "entries" | "detail";

async function fetchReflections(): Promise<Reflection[]> {
  const res = await fetch(`${API_URL}/reflections`);
  if (!res.ok) throw new Error("Failed to load reflections");
  return res.json();
}

async function createReflection(content: string): Promise<Reflection> {
  const res = await fetch(`${API_URL}/reflections`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ content }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.error ?? "Failed to save");
  }
  return res.json();
}

async function transcribeAudio(uri: string): Promise<string> {
  const body = new FormData();
  body.append("audio", {
    uri,
    name: "recording.m4a",
    type: "audio/m4a",
  } as unknown as Blob);

  const res = await fetch(`${API_URL}/transcriptions`, {
    method: "POST",
    body,
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.error ?? "Unable to transcribe");
  }

  const parsed = (await res.json()) as { text?: string };
  return (parsed.text ?? "").trim();
}

function formatDuration(seconds: number): string {
  const minutes = Math.floor(seconds / 60)
    .toString()
    .padStart(2, "0");
  const remainingSeconds = (seconds % 60).toString().padStart(2, "0");
  return `${minutes}:${remainingSeconds}`;
}

function formatEntryDate(dateIso: string): string {
  const date = new Date(dateIso);
  return date.toLocaleString(undefined, {
    weekday: "short",
    month: "short",
    day: "numeric",
    hour: "numeric",
    minute: "2-digit",
  });
}

export function ReflectionScreen() {
  const [reflections, setReflections] = useState<Reflection[]>([]);
  const [mode, setMode] = useState<ScreenMode>("capture");
  const [input, setInput] = useState("");
  const [recording, setRecording] = useState<Audio.Recording | null>(null);
  const [recordingSeconds, setRecordingSeconds] = useState(0);
  const [transcribing, setTranscribing] = useState(false);
  const [selectedReflection, setSelectedReflection] = useState<Reflection | null>(
    null
  );
  const [loading, setLoading] = useState(true);
  const [sending, setSending] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const pulseAnim = useRef(new Animated.Value(1)).current;
  const spinAnim = useRef(new Animated.Value(0)).current;
  const isStoppingRef = useRef(false);

  const isRecording = !!recording;

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const list = await fetchReflections();
      setReflections(list);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Could not load");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  useEffect(() => {
    if (!isRecording) return;
    const timer = setInterval(() => {
      setRecordingSeconds((prev) => prev + 1);
    }, 1000);
    return () => clearInterval(timer);
  }, [isRecording]);

  useEffect(() => {
    if (recordingSeconds < MAX_RECORDING_SECONDS || !isRecording) return;
    if (isStoppingRef.current) return;
    void stopRecording();
  }, [recordingSeconds, isRecording]);

  useEffect(() => {
    if (!isRecording) {
      pulseAnim.setValue(1);
      return;
    }
    const pulse = Animated.loop(
      Animated.sequence([
        Animated.timing(pulseAnim, {
          toValue: 1.06,
          duration: 750,
          useNativeDriver: true,
          easing: Easing.inOut(Easing.ease),
        }),
        Animated.timing(pulseAnim, {
          toValue: 1,
          duration: 750,
          useNativeDriver: true,
          easing: Easing.inOut(Easing.ease),
        }),
      ])
    );
    pulse.start();
    return () => pulse.stop();
  }, [isRecording, pulseAnim]);

  useEffect(() => {
    if (!transcribing) {
      spinAnim.setValue(0);
      return;
    }
    const spin = Animated.loop(
      Animated.timing(spinAnim, {
        toValue: 1,
        duration: 2000,
        useNativeDriver: true,
        easing: Easing.linear,
      })
    );
    spin.start();
    return () => spin.stop();
  }, [transcribing, spinAnim]);

  useEffect(() => {
    return () => {
      if (!recording) return;
      void recording.stopAndUnloadAsync().catch(() => null);
    };
  }, [recording]);

  const send = async (contentOverride?: string) => {
    const content = (contentOverride ?? input).trim();
    if (!content || sending) return;
    setInput(content);
    setSending(true);
    setError(null);
    try {
      const created = await createReflection(content);
      setReflections((prev) => [created, ...prev]);
      setInput("");
      setMode("capture");
    } catch (e) {
      setError(e instanceof Error ? e.message : "Could not save");
    } finally {
      setSending(false);
    }
  };

  const startRecording = async () => {
    if (isRecording || transcribing) return;
    setError(null);
    await Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    try {
      const permission = await Audio.requestPermissionsAsync();
      if (!permission.granted) {
        setError("Microphone permission is required to record.");
        return;
      }
      await Audio.setAudioModeAsync({
        allowsRecordingIOS: true,
        playsInSilentModeIOS: true,
      });
      const next = new Audio.Recording();
      await next.prepareToRecordAsync(Audio.RecordingOptionsPresets.HIGH_QUALITY);
      await next.startAsync();
      setRecording(next);
      setRecordingSeconds(0);
    } catch {
      setError("Unable to start recording. Try again.");
    }
  };

  const stopRecording = async () => {
    if (!recording || transcribing || isStoppingRef.current) return;
    isStoppingRef.current = true;
    setError(null);
    setTranscribing(true);
    await Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);
    try {
      await recording.stopAndUnloadAsync();
      const uri = recording.getURI();
      setRecording(null);
      setRecordingSeconds(0);
      if (!uri) {
        throw new Error("Recording not available");
      }
      const transcript = await transcribeAudio(uri);
      if (!transcript) {
        throw new Error("Transcription was empty");
      }
      setInput(transcript);
      setMode("review");
    } catch (e) {
      setError(
        e instanceof Error
          ? e.message
          : "Unable to transcribe. Try recording again."
      );
    } finally {
      setTranscribing(false);
      isStoppingRef.current = false;
    }
  };

  const openEntries = async () => {
    await Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    setMode("entries");
  };

  const openDetail = async (item: Reflection) => {
    await Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    setSelectedReflection(item);
    setMode("detail");
  };

  const renderCapture = () => {
    const isWarning = recordingSeconds >= WARNING_SECONDS;
    const statusText = transcribing
      ? "Transcribing..."
      : isRecording
      ? `Recording... ${formatDuration(recordingSeconds)}`
      : "Tap to start";
    const statusColor = transcribing
      ? "#667eea"
      : isRecording
      ? "#dc2626"
      : "#667eea";
    const rotation = spinAnim.interpolate({
      inputRange: [0, 1],
      outputRange: ["0deg", "360deg"],
    });

    return (
      <View style={styles.captureContainer}>
        <Text style={styles.dateLabel}>
          {new Date().toLocaleDateString(undefined, {
            weekday: "long",
            month: "long",
            day: "numeric",
          })}
        </Text>
        <Text style={styles.promptLabel}>What's on your mind today?</Text>
        <Animated.View
          style={[
            styles.voiceButtonShadow,
            {
              transform: [{ scale: pulseAnim }, { rotate: transcribing ? rotation : "0deg" }],
            },
          ]}
        >
          <Pressable
            onPress={isRecording ? stopRecording : startRecording}
            disabled={transcribing || sending}
            style={styles.voicePressable}
          >
            <LinearGradient
              colors={
                isRecording
                  ? ["#ef4444", "#dc2626"]
                  : ["#667eea", "#764ba2"]
              }
              start={{ x: 0, y: 0 }}
              end={{ x: 1, y: 1 }}
              style={styles.voiceButton}
            >
              <Text style={styles.voiceButtonIcon}>
                {transcribing ? "⟳" : isRecording ? "■" : "🎤"}
              </Text>
            </LinearGradient>
          </Pressable>
        </Animated.View>
        <Text style={[styles.statusLabel, { color: statusColor }]}>{statusText}</Text>
        {isWarning ? (
          <Text style={styles.warningLabel}>Max length is 5:00 - wrapping soon.</Text>
        ) : null}
        <TouchableOpacity style={styles.pastEntriesLink} onPress={openEntries}>
          <Text style={styles.pastEntriesText}>View past entries</Text>
        </TouchableOpacity>
      </View>
    );
  };

  const renderReview = () => (
    <KeyboardAvoidingView
      style={styles.reviewContainer}
      behavior={Platform.OS === "ios" ? "padding" : undefined}
    >
      <View style={styles.reviewHeader}>
        <TouchableOpacity
          onPress={() => {
            setInput("");
            setMode("capture");
          }}
        >
          <Text style={styles.backAction}>Back</Text>
        </TouchableOpacity>
        <Text style={styles.reviewTitle}>Review Entry</Text>
        <View style={styles.reviewSpacer} />
      </View>
      <Text style={styles.reviewDate}>
        {new Date().toLocaleString(undefined, {
          month: "short",
          day: "numeric",
          hour: "numeric",
          minute: "2-digit",
        })}
      </Text>

      <TextInput
        style={styles.reviewInput}
        value={input}
        onChangeText={setInput}
        multiline
        autoFocus
        placeholder="Your transcription will appear here..."
        placeholderTextColor="#999"
        editable={!sending}
      />

      <View style={styles.reviewActions}>
        <TouchableOpacity
          style={styles.discardButton}
          onPress={() => {
            setInput("");
            setMode("capture");
          }}
          disabled={sending}
        >
          <Text style={styles.discardLabel}>Discard</Text>
        </TouchableOpacity>

        <Pressable
          style={styles.saveButton}
          onPress={() => void send()}
          disabled={sending || !input.trim()}
        >
          <LinearGradient
            colors={["#667eea", "#764ba2"]}
            start={{ x: 0, y: 0 }}
            end={{ x: 1, y: 1 }}
            style={[styles.saveGradient, (!input.trim() || sending) && styles.saveDisabled]}
          >
            <Text style={styles.saveLabel}>{sending ? "Saving..." : "Save"}</Text>
          </LinearGradient>
        </Pressable>
      </View>
    </KeyboardAvoidingView>
  );

  const renderEntries = () => (
    <View style={styles.entriesContainer}>
      <View style={styles.entriesHeader}>
        <TouchableOpacity onPress={() => setMode("capture")}>
          <Text style={styles.backAction}>Back</Text>
        </TouchableOpacity>
        <Text style={styles.entriesTitle}>Your Entries</Text>
        <View style={styles.reviewSpacer} />
      </View>

      {reflections.length === 0 ? (
        <View style={styles.emptyState}>
          <Text style={styles.emptyStateText}>Start capturing your first thought.</Text>
        </View>
      ) : (
        <FlatList
          data={reflections}
          keyExtractor={(item) => item.id}
          contentContainerStyle={styles.entriesList}
          renderItem={({ item }) => (
            <Pressable style={styles.entryCard} onPress={() => void openDetail(item)}>
              <Text style={styles.entryDate}>{formatEntryDate(item.createdAt)}</Text>
              <Text style={styles.entryPreview} numberOfLines={2}>
                {item.content}
              </Text>
            </Pressable>
          )}
        />
      )}
    </View>
  );

  const renderDetail = () => {
    if (!selectedReflection) {
      setMode("entries");
      return null;
    }
    return (
      <View style={styles.entriesContainer}>
        <View style={styles.entriesHeader}>
          <TouchableOpacity onPress={() => setMode("entries")}>
            <Text style={styles.backAction}>Back</Text>
          </TouchableOpacity>
          <Text style={styles.entriesTitle}>Entry</Text>
          <View style={styles.reviewSpacer} />
        </View>

        <View style={styles.detailCard}>
          <Text style={styles.entryDate}>{formatEntryDate(selectedReflection.createdAt)}</Text>
          <Text style={styles.detailContent}>{selectedReflection.content}</Text>
        </View>
      </View>
    );
  };

  return (
    <View style={styles.container}>
      {error ? (
        <View style={styles.errorBanner}>
          <Text style={styles.errorText}>{error}</Text>
        </View>
      ) : null}

      {loading ? (
        <View style={styles.emptyState}>
          <Text style={styles.statusLabel}>Loading entries...</Text>
        </View>
      ) : mode === "capture" ? (
        renderCapture()
      ) : mode === "review" ? (
        renderReview()
      ) : mode === "entries" ? (
        renderEntries()
      ) : (
        renderDetail()
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#f8f7f4",
  },
  errorBanner: {
    backgroundColor: "#fee2e2",
    padding: 12,
    marginHorizontal: 20,
    marginTop: 12,
    borderRadius: 12,
  },
  errorText: {
    color: "#991b1b",
    fontSize: 14,
  },
  captureContainer: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
    paddingHorizontal: 24,
    paddingTop: 24,
    paddingBottom: 32,
  },
  dateLabel: {
    position: "absolute",
    top: 24,
    fontSize: 16,
    color: "#666",
    fontWeight: "500",
  },
  promptLabel: {
    position: "absolute",
    top: "30%",
    fontSize: 18,
    color: "#2c2c2c",
    fontWeight: "400",
  },
  voiceButtonShadow: {
    shadowColor: "#667eea",
    shadowOpacity: 0.24,
    shadowRadius: 16,
    shadowOffset: { width: 0, height: 8 },
    elevation: 8,
  },
  voicePressable: {
    borderRadius: 60,
    overflow: "hidden",
  },
  voiceButton: {
    width: 120,
    height: 120,
    borderRadius: 60,
    alignItems: "center",
    justifyContent: "center",
  },
  voiceButtonIcon: {
    fontSize: 42,
    color: "#fff",
  },
  statusLabel: {
    marginTop: 20,
    fontSize: 15,
    fontWeight: "500",
  },
  warningLabel: {
    marginTop: 8,
    color: "#dc2626",
    fontSize: 14,
  },
  pastEntriesLink: {
    position: "absolute",
    bottom: 32,
  },
  pastEntriesText: {
    color: "#667eea",
    fontSize: 14,
    fontWeight: "500",
  },
  reviewContainer: {
    flex: 1,
    paddingHorizontal: 20,
    paddingTop: 24,
    paddingBottom: Platform.OS === "ios" ? 24 : 16,
    backgroundColor: "#f8f7f4",
  },
  reviewHeader: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
  },
  backAction: {
    fontSize: 16,
    color: "#667eea",
    fontWeight: "600",
  },
  reviewTitle: {
    fontSize: 20,
    color: "#2c2c2c",
    fontWeight: "600",
  },
  reviewSpacer: {
    width: 40,
  },
  reviewDate: {
    marginTop: 8,
    marginBottom: 16,
    color: "#999",
    fontSize: 14,
    textAlign: "center",
  },
  reviewInput: {
    flex: 1,
    backgroundColor: "#fff",
    borderColor: "#e5e7eb",
    borderWidth: 1,
    borderRadius: 16,
    padding: 20,
    fontSize: 16,
    color: "#2c2c2c",
    lineHeight: 26,
    textAlignVertical: "top",
  },
  reviewActions: {
    flexDirection: "row",
    gap: 12,
    marginTop: 16,
  },
  discardButton: {
    flex: 1,
    backgroundColor: "#f3f4f6",
    borderRadius: 12,
    paddingVertical: 16,
    alignItems: "center",
  },
  discardLabel: {
    color: "#666",
    fontSize: 16,
    fontWeight: "600",
  },
  saveButton: {
    flex: 1,
    borderRadius: 12,
    overflow: "hidden",
  },
  saveGradient: {
    paddingVertical: 16,
    alignItems: "center",
  },
  saveDisabled: {
    opacity: 0.5,
  },
  saveLabel: {
    color: "#fff",
    fontSize: 16,
    fontWeight: "600",
  },
  entriesContainer: {
    flex: 1,
    backgroundColor: "#f8f7f4",
  },
  entriesHeader: {
    paddingTop: 24,
    paddingHorizontal: 20,
    paddingBottom: 16,
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
  },
  entriesTitle: {
    fontSize: 20,
    color: "#2c2c2c",
    fontWeight: "600",
  },
  entriesList: {
    paddingHorizontal: 20,
    paddingBottom: 20,
  },
  entryCard: {
    backgroundColor: "#fff",
    borderRadius: 12,
    padding: 16,
    marginBottom: 12,
    shadowColor: "#000",
    shadowOpacity: 0.06,
    shadowRadius: 8,
    shadowOffset: { width: 0, height: 4 },
    elevation: 2,
  },
  entryDate: {
    fontSize: 12,
    color: "#999",
    marginBottom: 8,
  },
  entryPreview: {
    fontSize: 16,
    color: "#2c2c2c",
    lineHeight: 24,
  },
  detailCard: {
    marginHorizontal: 20,
    backgroundColor: "#fff",
    borderRadius: 12,
    padding: 20,
  },
  detailContent: {
    fontSize: 16,
    color: "#2c2c2c",
    lineHeight: 26,
  },
  emptyState: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
    paddingHorizontal: 24,
  },
  emptyStateText: {
    color: "#666",
    fontSize: 16,
    textAlign: "center",
  },
});

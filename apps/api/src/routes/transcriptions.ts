import type { FastifyInstance } from "fastify";
import OpenAI from "openai";
import { toFile } from "openai/uploads";

const openAiApiKey = process.env.OPENAI_API_KEY;
const openai = openAiApiKey ? new OpenAI({ apiKey: openAiApiKey }) : null;

type TranscriptionResponse = {
  text: string;
};

function extensionFromMimeType(mimeType: string): string {
  if (mimeType.includes("m4a")) return "m4a";
  if (mimeType.includes("aac")) return "aac";
  if (mimeType.includes("webm")) return "webm";
  if (mimeType.includes("wav")) return "wav";
  if (mimeType.includes("mpeg")) return "mp3";
  return "m4a";
}

export async function transcriptionsRoutes(app: FastifyInstance) {
  app.post<{ Reply: TranscriptionResponse | { error: string } }>(
    "/",
    async (req, reply) => {
      if (!openai) {
        return reply.status(500).send({
          error: "OPENAI_API_KEY is not configured",
        });
      }

      const file = await req.file();
      if (!file) {
        return reply.status(400).send({ error: "audio file is required" });
      }

      const buffer = await file.toBuffer();
      if (!buffer.length) {
        return reply.status(400).send({ error: "audio file is empty" });
      }

      try {
        const ext = extensionFromMimeType(file.mimetype);
        const upload = await toFile(buffer, `recording.${ext}`);
        const result = await openai.audio.transcriptions.create({
          file: upload,
          model: "gpt-4o-mini-transcribe",
        });

        return reply.send({ text: result.text?.trim() ?? "" });
      } catch {
        return reply.status(502).send({
          error: "Unable to transcribe audio right now",
        });
      }
    }
  );
}

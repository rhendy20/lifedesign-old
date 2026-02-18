import Fastify from "fastify";
import cors from "@fastify/cors";
import multipart from "@fastify/multipart";
import { reflectionsRoutes } from "./routes/reflections.js";
import { transcriptionsRoutes } from "./routes/transcriptions.js";

const app = Fastify({ logger: true });

await app.register(cors, { origin: true });
await app.register(multipart, {
  limits: {
    fileSize: 15 * 1024 * 1024,
  },
});

await app.register(reflectionsRoutes, { prefix: "/reflections" });
await app.register(transcriptionsRoutes, { prefix: "/transcriptions" });

const port = Number(process.env.API_PORT) || 3000;
await app.listen({ port, host: "0.0.0.0" });
console.log(`API listening on http://localhost:${port}`);

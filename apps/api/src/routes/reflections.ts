import type { FastifyInstance, FastifyRequest, FastifyReply } from "fastify";
import { prisma } from "../lib/prisma.js";

// Stub: replace with OAuth when implementing auth slice.
const STUB_USER_ID = "dev-user-1";

function getUserId(_req: FastifyRequest): string {
  // TODO: read from OAuth token / session
  return STUB_USER_ID;
}

export async function reflectionsRoutes(app: FastifyInstance) {
  app.get("/", async (req: FastifyRequest, reply: FastifyReply) => {
    const userId = getUserId(req);
    const list = await prisma.reflection.findMany({
      where: { userId },
      orderBy: { createdAt: "desc" },
    });
    return reply.send(
      list.map((r) => ({
        id: r.id,
        userId: r.userId,
        content: r.content,
        createdAt: r.createdAt.toISOString(),
      }))
    );
  });

  app.post<{
    Body: { content?: string };
  }>("/", async (req, reply) => {
    const userId = getUserId(req);
    const content = req.body?.content?.trim();
    if (!content) {
      return reply.status(400).send({ error: "content is required" });
    }
    const reflection = await prisma.reflection.create({
      data: { userId, content },
    });
    return reply.status(201).send({
      id: reflection.id,
      userId: reflection.userId,
      content: reflection.content,
      createdAt: reflection.createdAt.toISOString(),
    });
  });
}

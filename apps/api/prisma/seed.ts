import { PrismaClient } from "@prisma/client";

const prisma = new PrismaClient();

async function main() {
  // Stub user id for local dev until OAuth exists
  const stubUserId = "dev-user-1";
  const existing = await prisma.reflection.findFirst({ where: { userId: stubUserId } });
  if (!existing) {
    await prisma.reflection.create({
      data: {
        userId: stubUserId,
        content: "My first reflection — life design starts with noticing.",
      },
    });
    console.log("Seed: created one sample reflection.");
  } else {
    console.log("Seed: sample reflection already exists.");
  }
}

main()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  })
  .finally(() => prisma.$disconnect());

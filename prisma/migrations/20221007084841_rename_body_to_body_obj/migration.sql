/*
  Warnings:

  - You are about to drop the column `body` on the `posts` table. All the data in the column will be lost.
  - Added the required column `body_obj` to the `posts` table without a default value. This is not possible if the table is not empty.

*/
-- AlterTable
ALTER TABLE "posts" DROP COLUMN "body",
ADD COLUMN     "body_obj" JSONB NOT NULL;

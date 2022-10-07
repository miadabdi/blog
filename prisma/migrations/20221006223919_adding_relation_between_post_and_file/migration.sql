/*
  Warnings:

  - You are about to drop the column `cover_image` on the `posts` table. All the data in the column will be lost.
  - A unique constraint covering the columns `[cover_image_file_id]` on the table `posts` will be added. If there are existing duplicate values, this will fail.

*/
-- AlterTable
ALTER TABLE "posts" DROP COLUMN "cover_image",
ADD COLUMN     "cover_image_file_id" INTEGER;

-- CreateIndex
CREATE UNIQUE INDEX "posts_cover_image_file_id_key" ON "posts"("cover_image_file_id");

-- AddForeignKey
ALTER TABLE "posts" ADD CONSTRAINT "posts_cover_image_file_id_fkey" FOREIGN KEY ("cover_image_file_id") REFERENCES "File"("id") ON DELETE SET NULL ON UPDATE CASCADE;

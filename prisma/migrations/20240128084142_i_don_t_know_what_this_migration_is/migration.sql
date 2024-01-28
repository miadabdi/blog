-- AlterTable
ALTER TABLE "categories_on_posts" RENAME CONSTRAINT "CategoriesOnPosts_pkey" TO "categories_on_posts_pkey";

-- AlterTable
ALTER TABLE "tags_on_posts" RENAME CONSTRAINT "TagsOnPosts_pkey" TO "tags_on_posts_pkey";

-- RenameForeignKey
ALTER TABLE "categories_on_posts" RENAME CONSTRAINT "CategoriesOnPosts_categoryId_fkey" TO "categories_on_posts_categoryId_fkey";

-- RenameForeignKey
ALTER TABLE "categories_on_posts" RENAME CONSTRAINT "CategoriesOnPosts_postId_fkey" TO "categories_on_posts_postId_fkey";

-- RenameForeignKey
ALTER TABLE "tags_on_posts" RENAME CONSTRAINT "TagsOnPosts_postId_fkey" TO "tags_on_posts_postId_fkey";

-- RenameForeignKey
ALTER TABLE "tags_on_posts" RENAME CONSTRAINT "TagsOnPosts_tagId_fkey" TO "tags_on_posts_tagId_fkey";

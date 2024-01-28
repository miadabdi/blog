import { AbilityBuilder, AbilityClass } from '@casl/ability';
import { PrismaAbility, Subjects } from '@casl/prisma';
import { Injectable } from '@nestjs/common';
import { Category, Comment, Post, Tag, User } from '@prisma/client';

export enum CaslAction {
	Manage = 'manage',
	Create = 'create',
	Read = 'read',
	Update = 'update',
	Delete = 'delete',
}

type AppAbility = PrismaAbility<
	[
		string,
		Subjects<{
			User: User;
			Post: Post;
			Comment: Comment;
			Category: Category;
			Tag: Tag;
		}>,
	]
>;
const AppAbility = PrismaAbility as AbilityClass<AppAbility>;

@Injectable()
export class CaslAbilityFactory {
	createForUser(user: User) {
		const { can, cannot, build } = new AbilityBuilder(AppAbility);

		if (user.isAdmin) {
			can(CaslAction.Manage, 'all'); // read-write access to everything
		} else {
			can(CaslAction.Read, 'all'); // read-only access to everything

			cannot(CaslAction.Create, 'Category').because('Only admins can create categories');
			cannot(CaslAction.Update, 'Category').because('Only admins can update categories');
			cannot(CaslAction.Delete, 'Category').because('Only admins can delete categories');

			cannot(CaslAction.Create, 'Tag').because('Only admins can create tags');
			cannot(CaslAction.Update, 'Tag').because('Only admins can update tags');
			cannot(CaslAction.Delete, 'Tag').because('Only admins can delete tags');

			can(CaslAction.Update, 'Post');
			cannot(CaslAction.Update, 'Post', { authorId: { not: user.id } }).because(
				`You cannot update posts you don't own`,
			);

			can(CaslAction.Delete, 'Post');
			cannot(CaslAction.Delete, 'Post', { authorId: { not: user.id } }).because(
				`You cannot delete posts you don't own`,
			);
			cannot(CaslAction.Delete, 'Post', { isPublished: true }).because(
				'Published posts can only be deleted by admins',
			);

			can(CaslAction.Update, 'Comment');
			cannot(CaslAction.Update, 'Comment', { authorId: { not: user.id } }).because(
				`You cannot update comments you don't own`,
			);

			can(CaslAction.Delete, 'Comment');
			cannot(CaslAction.Delete, 'Comment', { authorId: { not: user.id } }).because(
				`You cannot delete comments you don't own`,
			);
		}

		// return build({
		// 	// Read https://casl.js.org/v5/en/guide/subject-type-detection#use-classes-as-subject-types for details
		// 	detectSubjectType: (item) => item.constructor as ExtractSubjectType<Subjects>,
		// });
		return build();
	}
}

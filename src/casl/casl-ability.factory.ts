import { AbilityBuilder, AbilityClass } from '@casl/ability';
import { PrismaAbility, Subjects } from '@casl/prisma';
import { Injectable } from '@nestjs/common';
import { Post, User } from '@prisma/client';

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
			cannot(CaslAction.Create, 'all').because('Only admins can create');
			cannot(CaslAction.Update, 'all').because('Only admins can update');
			cannot(CaslAction.Delete, 'all').because('Only admins can delete');
		}

		// can(CaslAction.Update, 'Post', { authorId: user.id });
		// cannot(CaslAction.Delete, 'Post', { isPublished: true });

		// return build({
		// 	// Read https://casl.js.org/v5/en/guide/subject-type-detection#use-classes-as-subject-types for details
		// 	detectSubjectType: (item) => item.constructor as ExtractSubjectType<Subjects>,
		// });
		return build();
	}
}

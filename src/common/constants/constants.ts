export const JWT_COOKIE_NAME = 'access_token';
export const JWT_STRATEGY_NAME = 'jwt';
export const ROUTE_TIMEOUT = 30000;
export const LOG_LEVELS = {
	error: 1,
	warn: 1,
	info: 1,
	debug: 1,
	verbose: 1,
} as const;
export const API_PREFIX = 'api';
export const BUCKETS = [
	{
		name: 'images',
		policy: {
			Version: '2012-10-17',
			Statement: [
				{
					Sid: 'PublicRead',
					Effect: 'Allow',
					Principal: '*',
					Action: ['s3:GetObject', 's3:GetObjectVersion'],
					Resource: [`arn:aws:s3:::images/*`],
				},
			],
		},
		allowedMimeTypes: ['image/apng', 'image/avif', 'image/gif', 'image/jpeg', 'image/png', 'image/webp'],
	},
	{
		name: 'public',
		policy: {
			Version: '2012-10-17',
			Statement: [
				{
					Sid: 'PublicRead',
					Effect: 'Allow',
					Principal: '*',
					Action: ['s3:GetObject', 's3:GetObjectVersion'],
					Resource: [`arn:aws:s3:::public/*`],
				},
			],
		},
		allowedMimeTypes: [
			'image/apng',
			'image/avif',
			'image/gif',
			'image/jpeg',
			'image/png',
			'image/webp',
			'application/octet-stream',
			'text/plain',
			'text/css',
			'text/html',
			'text/javascript',
			'application/javascript',
		],
	},
] as const;
export const BUCKET_NAMES = BUCKETS.map((bucket) => bucket.name);
export type BUCKET_NAMES_TYPE = (typeof BUCKET_NAMES)[0];

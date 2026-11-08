import * as z from "zod";

export const TokenSchema = z.object({
  accessToken: z.string(),
  tokenType: z.string(),
});

export type Token = z.infer<typeof TokenSchema>;

export const MovieSchema = z.object({
  movieId: z.number(),
  title: z.string(),
  genres: z.string(),
  tmdbId: z.number(),
  picUrl: z.nullable(z.string()),
});

export type Movie = z.infer<typeof MovieSchema>;

export const ReviewSchema = z.object({
  reviewId: z.number(),
  userId: z.number(),
  movieId: z.number(),
  rating: z.number(),
});

export type Review = z.infer<typeof ReviewSchema>;

export const MovieAndReviewSchema = MovieSchema.extend({
  review: ReviewSchema.nullable(),
});

export type MovieAndReview = z.infer<typeof MovieAndReviewSchema>;

export const RecommendedMovieSchema = MovieSchema.extend({
  expectedScore: z.number(),
});

export type RecommendedMovie = z.infer<typeof RecommendedMovieSchema>;

export const UserSchema = z.object({
  userId: z.number(),
  email: z.nullable(z.string()),
  username: z.string(),
  isDisabled: z.boolean(),
});

export type User = z.infer<typeof UserSchema>;

/*
export interface ratingInfo {
  token: string;
  movieId: number;
  movieTitle: string;
  prevRating: number | null;
}
  */

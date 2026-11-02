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
  picUrl: z.string(),
});

export type Movie = z.infer<typeof MovieSchema>;

export const RatingSchema = z.object({
  ratingId: z.number(),
  movieId: z.number(),
  rating: z.number(),
});

export type Rating = z.infer<typeof RatingSchema>;

/*
export interface ratingInfo {
  token: string;
  movieId: number;
  movieTitle: string;
  prevRating: number | null;
}
  */

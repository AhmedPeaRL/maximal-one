/**
 * Records linguistic presence without response.
 */

export function record(entry) {
  return {
    content: entry,
    recordedAt: new Date().toISOString(),
    status: "unanswered"
  };
}

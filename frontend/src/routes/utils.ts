export function sanitizeInput(input: string): string {
  // Remove any HTML tags
  let sanitized = input.replace(/<[^>]*>?/gm, '');
  // Trim whitespace
  sanitized = sanitized.trim();
  // You can add more sanitization rules here
  return sanitized;
}
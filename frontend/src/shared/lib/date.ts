/**
 * Centralized date formatting utilities
 * All dates must use the standardized format: dd.mm.YYYY
 */

/**
 * Format a timestamp or Date to the standard format: dd.mm.YYYY
 * @param timestamp - Unix timestamp (seconds) or Date object
 * @returns Formatted date string (e.g., "01.01.2024")
 */
export function formatDate(timestamp: number | Date): string {
  const date = timestamp instanceof Date ? timestamp : new Date(timestamp * 1000);
  
  const day = date.getDate().toString().padStart(2, '0');
  const month = (date.getMonth() + 1).toString().padStart(2, '0');
  const year = date.getFullYear().toString();
  
  return `${day}.${month}.${year}`;
}

/**
 * Format a timestamp or Date with time to the standard format: dd.mm.YYYY HH:MM
 * @param timestamp - Unix timestamp (seconds) or Date object
 * @returns Formatted date-time string (e.g., "01.01.2024 15:30")
 */
export function formatDateTime(timestamp: number | Date): string {
  const date = timestamp instanceof Date ? timestamp : new Date(timestamp * 1000);
  
  const dateStr = formatDate(date);
  const hours = date.getHours().toString().padStart(2, '0');
  const minutes = date.getMinutes().toString().padStart(2, '0');
  
  return `${dateStr} ${hours}:${minutes}`;
}
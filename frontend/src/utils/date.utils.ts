export const formatDate = (dateInput: Date | string, formatType: 'short' | 'full' = 'short') => {
  const date = dateInput instanceof Date ? dateInput : new Date(dateInput)
  
  if (formatType === 'full') {
    return new Intl.DateTimeFormat('en-US', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    }).format(date)
  }
  
  // Default 'short' format
  const options: Intl.DateTimeFormatOptions = {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  }
  return date.toLocaleDateString(undefined, options)
}

// Convenience function for full date format
export const formatDateFull = (dateInput: Date | string) => {
  return formatDate(dateInput, 'full')
}

export const formatTime = (dateInput: Date | string, isMilitary: boolean = false) => {
  const date = dateInput instanceof Date ? dateInput : new Date(dateInput)
  return new Intl.DateTimeFormat('en-US', {
    hour: 'numeric',
    minute: 'numeric',
    hour12: !isMilitary,
  }).format(date)
}
"use client"

import * as React from "react"
import { ChevronLeftIcon, ChevronRightIcon } from "@/shared/ui/icons"
import { Button } from "@/shared/ui/button"
import { cn } from "@/shared/lib/utils"

export interface DateRange {
  from: Date | undefined
  to?: Date | undefined
}

interface DateCalendarProps {
  selected?: DateRange
  onSelect?: (range: DateRange | undefined) => void
  className?: string
}

// Helper function to format date as DD.MM.YYYY
const formatDateDisplay = (date: Date): string => {
  const day = String(date.getDate()).padStart(2, '0')
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const year = date.getFullYear()
  return `${day}.${month}.${year}`
}

// Helper to get days in month
const getDaysInMonth = (year: number, month: number) => {
  return new Date(year, month + 1, 0).getDate()
}

// Helper to get first day of month (0 = Monday, 1 = Tuesday, etc.)
const getFirstDayOfMonth = (year: number, month: number) => {
  const jsDay = new Date(year, month, 1).getDay()
  // Convert JS day (0=Sunday, 1=Monday...) to Monday-first (0=Monday, 1=Tuesday...)
  return (jsDay + 6) % 7
}

// Helper to check if date is same day
const isSameDay = (date1: Date, date2: Date) => {
  return date1.getDate() === date2.getDate() &&
         date1.getMonth() === date2.getMonth() &&
         date1.getFullYear() === date2.getFullYear()
}

// Helper to check if date is between two dates
const isDateInRange = (date: Date, start?: Date, end?: Date) => {
  if (!start) return false
  if (!end) return isSameDay(date, start)
  return date >= start && date <= end
}

export function DateCalendar({
  className,
  selected,
  onSelect,
}: DateCalendarProps) {
  const [currentDate, setCurrentDate] = React.useState(new Date())

  const year = currentDate.getFullYear()
  const month = currentDate.getMonth()
  const daysInMonth = getDaysInMonth(year, month)
  const firstDayOfMonth = getFirstDayOfMonth(year, month)

  const monthNames = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
  ]

  const weekDays = ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su']

  const handlePrevMonth = () => {
    setCurrentDate(new Date(year, month - 1))
  }

  const handleNextMonth = () => {
    setCurrentDate(new Date(year, month + 1))
  }

  const handleDateClick = (day: number) => {
    const clickedDate = new Date(year, month, day)
    
    if (!selected?.from || (selected.from && selected.to)) {
      // Starting fresh selection
      onSelect?.({
        from: clickedDate,
        to: undefined
      })
    } else if (selected.from && !selected.to) {
      // Complete the range
      if (clickedDate >= selected.from) {
        onSelect?.({
          from: selected.from,
          to: clickedDate
        })
      } else {
        onSelect?.({
          from: clickedDate,
          to: selected.from
        })
      }
    }
  }

  const renderCalendarDays = () => {
    const days = []
    
    // Empty cells for days before the first day of the month
    for (let i = 0; i < firstDayOfMonth; i++) {
      days.push(
        <div key={`empty-${i}`} className="p-2" />
      )
    }
    
    // Days of the month
    for (let day = 1; day <= daysInMonth; day++) {
      const date = new Date(year, month, day)
      const isSelected = selected?.from && isSameDay(date, selected.from) ||
                        selected?.to && isSameDay(date, selected.to)
      const isInRange = isDateInRange(date, selected?.from, selected?.to)
      const isToday = isSameDay(date, new Date())
      
      days.push(
        <button
          key={day}
          onClick={() => handleDateClick(day)}
          className={cn(
            "p-2 text-sm rounded-[0.75rem] hover:bg-muted transition-colors",
            isSelected && "bg-primary text-primary-foreground hover:bg-primary/90",
            isInRange && !isSelected && "bg-primary/20",
            isToday && !isSelected && "bg-accent text-accent-foreground",
            "focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2"
          )}
        >
          {day}
        </button>
      )
    }
    
    return days
  }

  return (
    <div className={cn("space-y-4", className)}>
      {/* Header */}
      <div className="flex items-center justify-between">
        <Button
          variant="outline"
          size="sm"
          onClick={handlePrevMonth}
        >
          <ChevronLeftIcon size={16} />
        </Button>
        
        <div className="font-semibold">
          {monthNames[month]} {year}
        </div>
        
        <Button
          variant="outline"
          size="sm"
          onClick={handleNextMonth}
        >
          <ChevronRightIcon size={16} />
        </Button>
      </div>

      {/* Week days */}
      <div className="grid grid-cols-7 gap-1">
        {weekDays.map(day => (
          <div key={day} className="p-2 text-center text-sm font-medium text-muted-foreground">
            {day}
          </div>
        ))}
      </div>

      {/* Calendar days */}
      <div className="grid grid-cols-7 gap-1">
        {renderCalendarDays()}
      </div>

      {/* Selected range display */}
      {selected?.from && (
        <div className="text-sm text-center text-muted-foreground">
          {selected.to ? (
            `${formatDateDisplay(selected.from)} - ${formatDateDisplay(selected.to)}`
          ) : (
            `${formatDateDisplay(selected.from)}`
          )}
        </div>
      )}
    </div>
  )
}
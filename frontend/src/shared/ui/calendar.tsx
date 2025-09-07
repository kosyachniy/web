"use client"

import * as React from "react"
import { format } from "date-fns"
import { CalendarIcon } from "@/shared/ui/icons"
import { cn } from "@/shared/lib/utils"
import { Button } from "@/shared/ui/button"
import { Input } from "@/shared/ui/input"

export interface DateRange {
  from: Date | undefined
  to?: Date | undefined
}

interface CalendarRangeProps {
  selected?: DateRange
  onSelect?: (range: DateRange | undefined) => void
  className?: string
}

export function CalendarRange({
  className,
  selected,
  onSelect,
}: CalendarRangeProps) {
  const [fromDate, setFromDate] = React.useState<string>("")
  const [toDate, setToDate] = React.useState<string>("")

  React.useEffect(() => {
    if (selected?.from) {
      setFromDate(format(selected.from, "yyyy-MM-dd"))
    }
    if (selected?.to) {
      setToDate(format(selected.to, "yyyy-MM-dd"))
    }
  }, [selected])

  const handleFromDateChange = (value: string) => {
    setFromDate(value)
    const date = value ? new Date(value) : undefined
    onSelect?.({
      from: date,
      to: selected?.to
    })
  }

  const handleToDateChange = (value: string) => {
    setToDate(value)
    const date = value ? new Date(value) : undefined
    onSelect?.({
      from: selected?.from,
      to: date
    })
  }

  return (
    <div className={cn("space-y-4", className)}>
      <div className="space-y-2">
        <label className="text-sm font-medium">From Date</label>
        <Input
          type="date"
          value={fromDate}
          onChange={(e) => handleFromDateChange(e.target.value)}
        />
      </div>
      <div className="space-y-2">
        <label className="text-sm font-medium">To Date</label>
        <Input
          type="date"
          value={toDate}
          onChange={(e) => handleToDateChange(e.target.value)}
        />
      </div>
    </div>
  )
}

interface DateRangePickerProps {
  selected?: DateRange
  onSelect?: (range: DateRange | undefined) => void
  className?: string
  placeholder?: string
}

export function DateRangePicker({
  className,
  selected,
  onSelect,
  placeholder = "Pick a date range"
}: DateRangePickerProps) {
  const formatDateRange = (range: DateRange | undefined) => {
    if (!range) return placeholder
    if (range.from) {
      if (range.to) {
        return `${format(range.from, "MMM dd")} - ${format(range.to, "MMM dd")}`
      } else {
        return format(range.from, "MMM dd")
      }
    }
    return placeholder
  }

  return (
    <div className={cn("grid gap-2", className)}>
      <Button
        id="date"
        variant={"outline"}
        className={cn(
          "w-full justify-start text-left font-normal",
          !selected && "text-muted-foreground"
        )}
      >
        <CalendarIcon size={16} className="mr-2" />
        {formatDateRange(selected)}
      </Button>
    </div>
  )
}
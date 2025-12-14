"use client"

import type React from "react"

import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { cn } from "@/lib/utils"
import { ChevronRight } from "lucide-react"

interface Column<T> {
  key: keyof T | string
  header: string
  render?: (item: T) => React.ReactNode
  className?: string
}

interface DataTableProps<T> {
  data: T[]
  columns: Column<T>[]
  onRowClick?: (item: T) => void
  className?: string
}

export function DataTable<T extends { id: string }>({ data, columns, onRowClick, className }: DataTableProps<T>) {
  return (
    <div className={cn("rounded-lg border border-border", className)}>
      <Table>
        <TableHeader>
          <TableRow className="border-border hover:bg-transparent">
            {columns.map((column) => (
              <TableHead
                key={String(column.key)}
                className={cn("text-xs font-medium text-muted-foreground", column.className)}
              >
                {column.header}
              </TableHead>
            ))}
            {onRowClick && <TableHead className="w-8" />}
          </TableRow>
        </TableHeader>
        <TableBody>
          {data.map((item) => (
            <TableRow
              key={item.id}
              className={cn("border-border", onRowClick && "cursor-pointer hover:bg-accent")}
              onClick={() => onRowClick?.(item)}
            >
              {columns.map((column) => (
                <TableCell key={String(column.key)} className={cn("text-sm", column.className)}>
                  {column.render ? column.render(item) : String(item[column.key as keyof T] ?? "")}
                </TableCell>
              ))}
              {onRowClick && (
                <TableCell className="w-8">
                  <ChevronRight className="h-4 w-4 text-muted-foreground" />
                </TableCell>
              )}
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  )
}

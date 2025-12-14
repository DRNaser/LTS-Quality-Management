import { cn } from "@/lib/utils"
import type { ReactNode } from "react"

interface ChartCardProps {
  title: string
  subtitle?: string
  children: ReactNode
  className?: string
  action?: ReactNode
}

export function ChartCard({ title, subtitle, children, className, action }: ChartCardProps) {
  return (
    <div className={cn("rounded-lg border border-border bg-card p-4", className)}>
      <div className="mb-4 flex items-start justify-between">
        <div>
          <h3 className="text-sm font-medium text-card-foreground">{title}</h3>
          {subtitle && <p className="text-xs text-muted-foreground">{subtitle}</p>}
        </div>
        {action}
      </div>
      {children}
    </div>
  )
}

import { cn } from "@/lib/utils"
import { ArrowUpRight, ArrowDownRight, Minus } from "lucide-react"
import type { LucideIcon } from "lucide-react"

interface KPICardProps {
  title: string
  value: string | number
  subtitle?: string
  trend?: number
  trendLabel?: string
  icon?: LucideIcon
  variant?: "default" | "success" | "warning" | "danger"
}

export function KPICard({ title, value, subtitle, trend, trendLabel, icon: Icon, variant = "default" }: KPICardProps) {
  const getTrendIcon = () => {
    if (trend === undefined || trend === 0) return <Minus className="h-3 w-3" />
    return trend > 0 ? <ArrowUpRight className="h-3 w-3" /> : <ArrowDownRight className="h-3 w-3" />
  }

  const getTrendColor = () => {
    if (trend === undefined || trend === 0) return "text-muted-foreground"
    // For concession rate, down is good
    return trend < 0 ? "text-success" : "text-destructive"
  }

  const getVariantStyles = () => {
    switch (variant) {
      case "success":
        return "border-l-success"
      case "warning":
        return "border-l-warning"
      case "danger":
        return "border-l-danger"
      default:
        return "border-l-primary"
    }
  }

  return (
    <div className={cn("rounded-lg border border-border bg-card p-4 border-l-4", getVariantStyles())}>
      <div className="flex items-start justify-between">
        <div className="space-y-1">
          <p className="text-xs font-medium text-muted-foreground">{title}</p>
          <p className="text-2xl font-bold text-card-foreground">{value}</p>
          {subtitle && <p className="text-xs text-muted-foreground">{subtitle}</p>}
        </div>
        {Icon && (
          <div className="rounded-lg bg-secondary p-2">
            <Icon className="h-4 w-4 text-muted-foreground" />
          </div>
        )}
      </div>
      {trend !== undefined && (
        <div className={cn("mt-3 flex items-center gap-1 text-xs", getTrendColor())}>
          {getTrendIcon()}
          <span>{Math.abs(trend)}%</span>
          {trendLabel && <span className="text-muted-foreground">{trendLabel}</span>}
        </div>
      )}
    </div>
  )
}

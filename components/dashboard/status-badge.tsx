import { cn } from "@/lib/utils"

interface StatusBadgeProps {
  status: "success" | "warning" | "danger" | "neutral"
  label: string
  size?: "sm" | "md"
}

export function StatusBadge({ status, label, size = "sm" }: StatusBadgeProps) {
  const getStatusStyles = () => {
    switch (status) {
      case "success":
        return "bg-success/10 text-success border-success/20"
      case "warning":
        return "bg-warning/10 text-warning border-warning/20"
      case "danger":
        return "bg-danger/10 text-danger border-danger/20"
      default:
        return "bg-muted text-muted-foreground border-border"
    }
  }

  return (
    <span
      className={cn(
        "inline-flex items-center gap-1.5 rounded-full border font-medium",
        getStatusStyles(),
        size === "sm" ? "px-2 py-0.5 text-xs" : "px-3 py-1 text-sm",
      )}
    >
      <span
        className={cn(
          "h-1.5 w-1.5 rounded-full",
          status === "success" && "bg-success",
          status === "warning" && "bg-warning",
          status === "danger" && "bg-danger",
          status === "neutral" && "bg-muted-foreground",
        )}
      />
      {label}
    </span>
  )
}

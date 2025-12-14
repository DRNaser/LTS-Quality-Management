"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import { cn } from "@/lib/utils"
import {
  LayoutDashboard,
  Building2,
  Target,
  Search,
  AlertTriangle,
  Users,
  Upload,
  ChevronDown,
  Package,
} from "lucide-react"
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from "@/components/ui/collapsible"
import { useState } from "react"
import { depots } from "@/lib/mock-data"

const navigation = [
  { name: "Überblick", href: "/", icon: LayoutDashboard },
  { name: "Depot-Vergleich", href: "/depot-vergleich", icon: Building2 },
  { name: "Risikoanalyse", href: "/risikoanalyse", icon: Target },
  { name: "Mustererkennung", href: "/mustererkennung", icon: Search },
  { name: "Missbrauchserkennung", href: "/missbrauchserkennung", icon: AlertTriangle },
  { name: "Fahrerprofile", href: "/fahrerprofile", icon: Users },
  { name: "Datenverwaltung", href: "/datenverwaltung", icon: Upload },
]

export function Sidebar() {
  const pathname = usePathname()
  const [depotsOpen, setDepotsOpen] = useState(true)

  return (
    <aside className="fixed left-0 top-0 z-40 h-screen w-64 border-r border-sidebar-border bg-sidebar">
      <div className="flex h-full flex-col">
        {/* Logo */}
        <div className="flex h-16 items-center gap-3 border-b border-sidebar-border px-6">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-primary">
            <Package className="h-4 w-4 text-primary-foreground" />
          </div>
          <div>
            <h1 className="text-sm font-semibold text-sidebar-foreground">LTS Quality</h1>
            <p className="text-xs text-muted-foreground">Management Platform</p>
          </div>
        </div>

        {/* Navigation */}
        <nav className="flex-1 space-y-1 p-4">
          {navigation.map((item) => {
            const isActive = pathname === item.href
            return (
              <Link
                key={item.name}
                href={item.href}
                className={cn(
                  "flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors",
                  isActive
                    ? "bg-sidebar-accent text-sidebar-foreground"
                    : "text-muted-foreground hover:bg-sidebar-accent hover:text-sidebar-foreground",
                )}
              >
                <item.icon className="h-4 w-4" />
                {item.name}
              </Link>
            )
          })}
        </nav>

        {/* Depot Filter */}
        <div className="border-t border-sidebar-border p-4">
          <Collapsible open={depotsOpen} onOpenChange={setDepotsOpen}>
            <CollapsibleTrigger className="flex w-full items-center justify-between rounded-lg px-3 py-2 text-sm font-medium text-muted-foreground hover:bg-sidebar-accent hover:text-sidebar-foreground">
              <span className="flex items-center gap-3">
                <Building2 className="h-4 w-4" />
                Depots
              </span>
              <ChevronDown className={cn("h-4 w-4 transition-transform", depotsOpen && "rotate-180")} />
            </CollapsibleTrigger>
            <CollapsibleContent className="mt-1 space-y-1">
              {depots.map((depot) => (
                <button
                  key={depot.id}
                  className="flex w-full items-center gap-2 rounded-lg px-3 py-1.5 pl-10 text-xs text-muted-foreground hover:bg-sidebar-accent hover:text-sidebar-foreground"
                >
                  <span className="h-1.5 w-1.5 rounded-full bg-primary" />
                  {depot.name}
                </button>
              ))}
            </CollapsibleContent>
          </Collapsible>
        </div>

        {/* Footer */}
        <div className="border-t border-sidebar-border p-4">
          <div className="rounded-lg bg-sidebar-accent p-3">
            <p className="text-xs text-muted-foreground">Letzte Aktualisierung</p>
            <p className="text-sm font-medium text-sidebar-foreground">14.12.2024, 09:30</p>
          </div>
        </div>
      </div>
    </aside>
  )
}

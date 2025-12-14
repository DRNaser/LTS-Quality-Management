"use client"

import { useState } from "react"
import { Sidebar } from "@/components/dashboard/sidebar"
import { Header } from "@/components/dashboard/header"
import { KPICard } from "@/components/dashboard/kpi-card"
import { ChartCard } from "@/components/dashboard/chart-card"
import { StatusBadge } from "@/components/dashboard/status-badge"
import { abusePatterns } from "@/lib/mock-data"
import {
  AlertTriangle,
  MapPin,
  Users,
  FileWarning,
  Download,
  ChevronDown,
  ChevronRight,
  Flag,
  Clock,
  ExternalLink,
} from "lucide-react"
import { Button } from "@/components/ui/button"
import { Checkbox } from "@/components/ui/checkbox"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from "@/components/ui/collapsible"

interface ExtendedAbusePattern {
  id: string
  address: string
  zipCode: string
  occurrences: number
  drivers: number
  severity: "critical" | "high" | "medium" | "low"
  lastOccurrence: string
  pattern: string
  history?: {
    date: string
    driver: string
    type: string
    notes: string
  }[]
  customerInfo?: {
    totalOrders: number
    concessionClaims: number
    accountAge: string
  }
}

// Extended abuse patterns with history
const extendedPatterns: ExtendedAbusePattern[] = abusePatterns.map((p, i) => ({
  ...p,
  history: [
    {
      date: "2024-01-12",
      driver: "M. Schmidt",
      type: "Nachbar-Zustellung",
      notes: "Kunde nicht erreichbar trotz Terminvereinbarung",
    },
    {
      date: "2024-01-10",
      driver: "L. Weber",
      type: "Briefkasten",
      notes: "Klingel funktionierte angeblich nicht",
    },
    {
      date: "2024-01-08",
      driver: "A. Müller",
      type: "Nachbar-Zustellung",
      notes: "Keine Reaktion auf mehrfaches Klingeln",
    },
  ],
  customerInfo: {
    totalOrders: Math.floor(Math.random() * 100) + 50,
    concessionClaims: Math.floor(Math.random() * 30) + 10,
    accountAge: `${Math.floor(Math.random() * 3) + 1} Jahre`,
  },
}))

export default function AbuseDetectionPage() {
  const [selectedPatterns, setSelectedPatterns] = useState<Set<string>>(new Set())
  const [expandedPattern, setExpandedPattern] = useState<string | null>(null)
  const [severityFilter, setSeverityFilter] = useState<string>("all")

  const filteredPatterns =
    severityFilter === "all" ? extendedPatterns : extendedPatterns.filter((p) => p.severity === severityFilter)

  const togglePatternSelection = (id: string) => {
    const newSelection = new Set(selectedPatterns)
    if (newSelection.has(id)) {
      newSelection.delete(id)
    } else {
      newSelection.add(id)
    }
    setSelectedPatterns(newSelection)
  }

  const getSeverityStatus = (severity: string): "success" | "warning" | "danger" => {
    if (severity === "critical" || severity === "high") return "danger"
    if (severity === "medium") return "warning"
    return "success"
  }

  const getSeverityLabel = (severity: string): string => {
    switch (severity) {
      case "critical":
        return "Kritisch"
      case "high":
        return "Hoch"
      case "medium":
        return "Mittel"
      case "low":
        return "Niedrig"
      default:
        return severity
    }
  }

  const criticalCount = extendedPatterns.filter((p) => p.severity === "critical").length
  const highCount = extendedPatterns.filter((p) => p.severity === "high").length
  const totalOccurrences = extendedPatterns.reduce((sum, p) => sum + p.occurrences, 0)
  const uniqueDrivers = new Set(extendedPatterns.flatMap((p) => p.history?.map((h) => h.driver) || [])).size

  return (
    <div className="flex min-h-screen">
      <Sidebar />
      <main className="ml-64 flex-1">
        <Header title="Missbrauchserkennung" subtitle="Verdächtige Muster und Adressen" />

        <div className="p-6">
          {/* KPI Row */}
          <div className="mb-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            <KPICard
              title="Kritische Muster"
              value={criticalCount}
              subtitle="Sofortige Prüfung erforderlich"
              icon={AlertTriangle}
              variant="danger"
            />
            <KPICard
              title="Hochrisiko-Adressen"
              value={highCount}
              subtitle="Erhöhte Aufmerksamkeit"
              icon={MapPin}
              variant="warning"
            />
            <KPICard title="Betroffene Fahrer" value={uniqueDrivers} subtitle="In den letzten 30 Tagen" icon={Users} />
            <KPICard
              title="Gesamtvorfälle"
              value={totalOccurrences}
              subtitle="Alle erkannten Muster"
              icon={FileWarning}
            />
          </div>

          {/* Actions Bar */}
          <div className="mb-6 flex items-center justify-between">
            <div className="flex items-center gap-4">
              <Select value={severityFilter} onValueChange={setSeverityFilter}>
                <SelectTrigger className="w-[180px] border-border bg-secondary">
                  <SelectValue placeholder="Alle Schweregrade" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">Alle Schweregrade</SelectItem>
                  <SelectItem value="critical">Kritisch</SelectItem>
                  <SelectItem value="high">Hoch</SelectItem>
                  <SelectItem value="medium">Mittel</SelectItem>
                  <SelectItem value="low">Niedrig</SelectItem>
                </SelectContent>
              </Select>
              {selectedPatterns.size > 0 && (
                <span className="text-sm text-muted-foreground">{selectedPatterns.size} ausgewählt</span>
              )}
            </div>
            <div className="flex items-center gap-2">
              <Button
                variant="outline"
                size="sm"
                className="gap-2 bg-transparent"
                disabled={selectedPatterns.size === 0}
              >
                <Flag className="h-4 w-4" />
                Als untersucht markieren
              </Button>
              <Button variant="outline" size="sm" className="gap-2 bg-transparent">
                <Download className="h-4 w-4" />
                Export Report
              </Button>
            </div>
          </div>

          {/* Abuse Patterns List */}
          <ChartCard title="Erkannte Missbrauchsmuster" subtitle={`${filteredPatterns.length} verdächtige Adressen`}>
            <div className="space-y-3">
              {filteredPatterns.map((pattern) => (
                <Collapsible
                  key={pattern.id}
                  open={expandedPattern === pattern.id}
                  onOpenChange={() => setExpandedPattern(expandedPattern === pattern.id ? null : pattern.id)}
                >
                  <div className="rounded-lg border border-border bg-secondary/30 overflow-hidden">
                    {/* Header */}
                    <div className="flex items-center gap-4 p-4">
                      <Checkbox
                        checked={selectedPatterns.has(pattern.id)}
                        onCheckedChange={() => togglePatternSelection(pattern.id)}
                        onClick={(e) => e.stopPropagation()}
                      />

                      <CollapsibleTrigger className="flex flex-1 items-center gap-4 text-left">
                        <div className="flex-1">
                          <div className="flex items-center gap-2">
                            <MapPin className="h-4 w-4 text-primary" />
                            <span className="font-medium text-foreground">{pattern.address}</span>
                            <span className="text-sm text-muted-foreground">PLZ {pattern.zipCode}</span>
                          </div>
                          <p className="mt-1 text-sm text-muted-foreground">{pattern.pattern}</p>
                        </div>

                        <div className="flex items-center gap-6">
                          <div className="text-center">
                            <p className="text-lg font-bold text-foreground">{pattern.occurrences}</p>
                            <p className="text-xs text-muted-foreground">Vorfälle</p>
                          </div>
                          <div className="text-center">
                            <p className="text-lg font-bold text-foreground">{pattern.drivers}</p>
                            <p className="text-xs text-muted-foreground">Fahrer</p>
                          </div>
                          <StatusBadge
                            status={getSeverityStatus(pattern.severity)}
                            label={getSeverityLabel(pattern.severity)}
                          />
                          {expandedPattern === pattern.id ? (
                            <ChevronDown className="h-5 w-5 text-muted-foreground" />
                          ) : (
                            <ChevronRight className="h-5 w-5 text-muted-foreground" />
                          )}
                        </div>
                      </CollapsibleTrigger>
                    </div>

                    {/* Expanded Content */}
                    <CollapsibleContent>
                      <div className="border-t border-border bg-background/50 p-4">
                        <div className="grid gap-6 lg:grid-cols-2">
                          {/* History */}
                          <div>
                            <h4 className="mb-3 text-sm font-medium text-foreground flex items-center gap-2">
                              <Clock className="h-4 w-4" />
                              Vorfallhistorie
                            </h4>
                            <div className="space-y-2">
                              {pattern.history?.map((event, idx) => (
                                <div key={idx} className="rounded-lg bg-secondary/50 p-3">
                                  <div className="flex items-center justify-between mb-1">
                                    <span className="text-sm font-medium text-foreground">{event.driver}</span>
                                    <span className="text-xs text-muted-foreground">{event.date}</span>
                                  </div>
                                  <div className="flex items-center gap-2">
                                    <span className="inline-flex items-center rounded-full bg-primary/10 px-2 py-0.5 text-xs text-primary">
                                      {event.type}
                                    </span>
                                  </div>
                                  <p className="mt-1 text-xs text-muted-foreground">{event.notes}</p>
                                </div>
                              ))}
                            </div>
                          </div>

                          {/* Customer Info */}
                          <div>
                            <h4 className="mb-3 text-sm font-medium text-foreground flex items-center gap-2">
                              <Users className="h-4 w-4" />
                              Kundeninformationen
                            </h4>
                            <div className="rounded-lg bg-secondary/50 p-4">
                              <div className="grid grid-cols-3 gap-4 text-center">
                                <div>
                                  <p className="text-2xl font-bold text-foreground">
                                    {pattern.customerInfo?.totalOrders}
                                  </p>
                                  <p className="text-xs text-muted-foreground">Bestellungen</p>
                                </div>
                                <div>
                                  <p className="text-2xl font-bold text-destructive">
                                    {pattern.customerInfo?.concessionClaims}
                                  </p>
                                  <p className="text-xs text-muted-foreground">Konzessionen</p>
                                </div>
                                <div>
                                  <p className="text-2xl font-bold text-foreground">
                                    {pattern.customerInfo?.accountAge}
                                  </p>
                                  <p className="text-xs text-muted-foreground">Kontoalter</p>
                                </div>
                              </div>

                              {/* Abuse ratio indicator */}
                              <div className="mt-4">
                                <div className="flex items-center justify-between text-xs mb-1">
                                  <span className="text-muted-foreground">Missbrauchsquote</span>
                                  <span className="font-medium text-destructive">
                                    {pattern.customerInfo
                                      ? (
                                          (pattern.customerInfo.concessionClaims / pattern.customerInfo.totalOrders) *
                                          100
                                        ).toFixed(1)
                                      : 0}
                                    %
                                  </span>
                                </div>
                                <div className="h-2 rounded-full bg-secondary overflow-hidden">
                                  <div
                                    className="h-full rounded-full bg-destructive transition-all"
                                    style={{
                                      width: `${pattern.customerInfo ? (pattern.customerInfo.concessionClaims / pattern.customerInfo.totalOrders) * 100 : 0}%`,
                                    }}
                                  />
                                </div>
                              </div>
                            </div>

                            {/* Actions */}
                            <div className="mt-4 flex gap-2">
                              <Button variant="outline" size="sm" className="flex-1 bg-transparent">
                                <Flag className="h-4 w-4 mr-2" />
                                Untersuchen
                              </Button>
                              <Button variant="outline" size="sm" className="flex-1 bg-transparent">
                                <ExternalLink className="h-4 w-4 mr-2" />
                                Details
                              </Button>
                            </div>
                          </div>
                        </div>
                      </div>
                    </CollapsibleContent>
                  </div>
                </Collapsible>
              ))}
            </div>
          </ChartCard>

          {/* Summary Statistics */}
          <div className="mt-6">
            <ChartCard title="Zusammenfassung" subtitle="Übersicht der Missbrauchsmuster nach Schweregrad">
              <div className="grid gap-4 sm:grid-cols-4">
                {(["critical", "high", "medium", "low"] as const).map((severity) => {
                  const count = extendedPatterns.filter((p) => p.severity === severity).length
                  const totalForSeverity = extendedPatterns
                    .filter((p) => p.severity === severity)
                    .reduce((sum, p) => sum + p.occurrences, 0)

                  return (
                    <div key={severity} className="rounded-lg border border-border bg-secondary/30 p-4 text-center">
                      <StatusBadge status={getSeverityStatus(severity)} label={getSeverityLabel(severity)} />
                      <p className="mt-3 text-3xl font-bold text-foreground">{count}</p>
                      <p className="text-sm text-muted-foreground">Muster</p>
                      <p className="mt-2 text-xs text-muted-foreground">{totalForSeverity} Vorfälle insgesamt</p>
                    </div>
                  )
                })}
              </div>
            </ChartCard>
          </div>
        </div>
      </main>
    </div>
  )
}

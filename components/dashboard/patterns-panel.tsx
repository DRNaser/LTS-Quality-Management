"use client"

import { useEffect, useMemo, useState } from "react"
import Link from "next/link"
import { PatternDetection, TrendDetection } from "@/lib/pattern-analyzer"
import {
  ConcessionEvent,
  depots,
  generateConcessionEvents,
  generateDrivers,
} from "@/lib/mock-data"
import { StatusBadge } from "./status-badge"

const severityVariant: Record<PatternDetection["severity"], "success" | "warning" | "danger" | "neutral"> = {
  low: "success",
  medium: "warning",
  high: "danger",
  critical: "danger",
}

interface PatternsPanelProps {
  fetcher?: typeof fetch
  seedEvents?: ConcessionEvent[]
}

export function PatternsPanel({ fetcher = fetch, seedEvents }: PatternsPanelProps) {
  const drivers = useMemo(() => generateDrivers(30), [])
  const events = useMemo(() => seedEvents ?? generateConcessionEvents(180), [seedEvents])
  const [patterns, setPatterns] = useState<PatternDetection[]>([])
  const [trends, setTrends] = useState<TrendDetection[]>([])
  const [status, setStatus] = useState<"idle" | "loading" | "error" | "empty">("idle")
  const [errorMessage, setErrorMessage] = useState<string | null>(null)
  const [filters, setFilters] = useState({ depotId: "", driverId: "" })

  useEffect(() => {
    let cancelled = false
    async function loadPatterns() {
      setStatus("loading")
      setErrorMessage(null)

      try {
        const response = await fetcher("/api/patterns", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            events,
            filters: {
              depotId: filters.depotId || undefined,
              driverId: filters.driverId || undefined,
            },
          }),
        })

        const payload: any =
          typeof (response as any)?.json === "function"
            ? await (response as any).json()
            : response

        if (!payload?.patterns || !payload?.trends) {
          throw new Error("Invalid analyzer response")
        }

        if (cancelled) return
        setPatterns(payload.patterns)
        setTrends(payload.trends)
        setStatus(payload.patterns.length === 0 ? "empty" : "idle")
      } catch (error) {
        console.error("Failed to load patterns", error)
        if (cancelled) return
        setStatus("error")
        setErrorMessage(error instanceof Error ? error.message : "Unbekannter Fehler")
      }
    }

    loadPatterns()
    return () => {
      cancelled = true
    }
  }, [events, fetcher, filters.depotId, filters.driverId])

  const getTrendForDriver = (driverId: string) =>
    trends.find((trend) => trend.driverId === driverId)

  return (
    <div className="rounded-lg border border-border bg-card p-4 shadow-sm" data-testid="patterns-panel">
      <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
        <div>
          <h2 className="text-xl font-semibold text-foreground">Muster & Trends</h2>
          <p className="text-sm text-muted-foreground">
            Erkennt automatisch Auffälligkeiten aus Konzessionsereignissen
          </p>
        </div>
        <div className="flex gap-2">
          <select
            aria-label="Depot Filter"
            data-testid="depot-filter"
            className="min-w-[180px] rounded-md border border-border bg-background px-3 py-2 text-sm"
            value={filters.depotId}
            onChange={(event) => setFilters((prev) => ({ ...prev, depotId: event.target.value }))}
          >
            <option value="">Alle Depots</option>
            {depots.map((depot) => (
              <option key={depot.id} value={depot.id}>
                {depot.name}
              </option>
            ))}
          </select>
          <select
            aria-label="Fahrer Filter"
            data-testid="driver-filter"
            className="min-w-[180px] rounded-md border border-border bg-background px-3 py-2 text-sm"
            value={filters.driverId}
            onChange={(event) => setFilters((prev) => ({ ...prev, driverId: event.target.value }))}
          >
            <option value="">Alle Fahrer</option>
            {drivers.map((driver) => (
              <option key={driver.id} value={driver.id}>
                {driver.name} ({driver.id})
              </option>
            ))}
          </select>
        </div>
      </div>

      <div className="mt-4 divide-y divide-border" data-testid="pattern-results">
        {status === "loading" && (
          <div className="py-6 text-sm text-muted-foreground">Lade Muster...</div>
        )}

        {status === "error" && (
          <div className="py-6 text-sm text-destructive" data-testid="error-state">
            Muster konnten nicht geladen werden: {errorMessage}
          </div>
        )}

        {status === "empty" && (
          <div className="py-6 text-sm text-muted-foreground" data-testid="empty-state">
            Keine Muster für die aktuelle Auswahl gefunden.
          </div>
        )}

        {status === "idle" &&
          patterns.map((pattern) => {
            const topDriver = pattern.drivers[0]
            const trend = topDriver ? getTrendForDriver(topDriver) : undefined

            return (
              <div key={pattern.id} className="grid gap-2 py-4 md:grid-cols-[2fr,1fr] md:items-center">
                <div>
                  <div className="flex items-center gap-2">
                    <StatusBadge status={severityVariant[pattern.severity]} label={pattern.severity.toUpperCase()} />
                    <span className="text-xs text-muted-foreground">{(pattern.confidence * 100).toFixed(0)}% Vertrauen</span>
                  </div>
                  <h3 className="mt-1 text-base font-semibold text-foreground">{pattern.type}</h3>
                  <p className="text-sm text-muted-foreground">{pattern.description}</p>
                  <div className="mt-2 flex flex-wrap gap-2 text-xs">
                    {pattern.drivers.map((driverId) => (
                      <Link
                        key={driverId}
                        className="rounded-md bg-muted px-2 py-1 text-foreground hover:bg-muted/80"
                        href={`/fahrerprofile?driverId=${driverId}`}
                      >
                        Fahrer {driverId}
                      </Link>
                    ))}
                    {pattern.depotId && (
                      <span className="rounded-md bg-primary/10 px-2 py-1 text-primary">
                        Depot {pattern.depotId}
                      </span>
                    )}
                  </div>
                </div>

                {trend && (
                  <div className="rounded-md bg-muted/40 p-3 text-sm" data-testid="trend-summary">
                    <div className="text-xs text-muted-foreground">Trend ({trend.driverId})</div>
                    <div className="text-foreground">
                      {trend.direction === "increasing" && "Steigend"}
                      {trend.direction === "decreasing" && "Sinkend"}
                      {trend.direction === "stable" && "Stabil"}
                    </div>
                    <div className="text-xs text-muted-foreground">Änderung: {trend.change}%</div>
                    <div className="text-xs text-muted-foreground">Signifikanz: {trend.significance}</div>
                  </div>
                )}
              </div>
            )
          })}
      </div>
    </div>
  )
}

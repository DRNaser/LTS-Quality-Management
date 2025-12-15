export interface ConcessionEvent {
  id: string
  driverId: string
  depotId: string
  timestamp: string
  isConcession: boolean
  type?: string
}

export interface PatternDetection {
  id: string
  type: string
  description: string
  severity: "low" | "medium" | "high" | "critical"
  confidence: number
  drivers: string[]
  depotId?: string
}

export interface TrendDetection {
  driverId: string
  direction: "increasing" | "decreasing" | "stable"
  change: number
  significance: number
}

export interface AnalyzerFilters {
  depotId?: string
  driverId?: string
}

export interface AnalyzerResponse {
  patterns: PatternDetection[]
  trends: TrendDetection[]
}

export const cleanConcessionEvents = (
  events: ConcessionEvent[],
  filters: AnalyzerFilters = {}
): ConcessionEvent[] => {
  return events
    .filter((event) => Boolean(event.driverId) && Boolean(event.depotId) && Boolean(event.timestamp))
    .filter((event) =>
      filters.depotId ? event.depotId === filters.depotId : true
    )
    .filter((event) =>
      filters.driverId ? event.driverId === filters.driverId : true
    )
    .map((event) => ({
      ...event,
      isConcession: Boolean(event.isConcession),
      timestamp: new Date(event.timestamp).toISOString(),
    }))
}

const determineSeverity = (rate: number): PatternDetection["severity"] => {
  if (rate >= 0.18) return "critical"
  if (rate >= 0.12) return "high"
  if (rate >= 0.07) return "medium"
  return "low"
}

export class PatternAnalyzer {
  analyze(
    events: ConcessionEvent[],
    filters: AnalyzerFilters = {}
  ): AnalyzerResponse {
    const cleaned = cleanConcessionEvents(events, filters)

    if (cleaned.length === 0) {
      return { patterns: [], trends: [] }
    }

    const byDriver: Record<string, ConcessionEvent[]> = {}
    const byDepot: Record<string, ConcessionEvent[]> = {}

    cleaned.forEach((event) => {
      byDriver[event.driverId] = byDriver[event.driverId] || []
      byDriver[event.driverId].push(event)

      byDepot[event.depotId] = byDepot[event.depotId] || []
      byDepot[event.depotId].push(event)
    })

    const patterns: PatternDetection[] = []

    Object.entries(byDriver).forEach(([driverId, driverEvents]) => {
      const concessionCount = driverEvents.filter((event) => event.isConcession).length
      const rate = concessionCount / driverEvents.length
      const severity = determineSeverity(rate)

      if (rate > 0.05) {
        patterns.push({
          id: `driver-${driverId}`,
          type: "driver_hotspot",
          description: `Fahrer ${driverId} zeigt erhöhte Konzessionsrate (${(rate * 100).toFixed(1)}%)`,
          severity,
          confidence: Math.min(1, Math.max(0.5, rate)),
          drivers: [driverId],
          depotId: driverEvents[0]?.depotId,
        })
      }
    })

    Object.entries(byDepot).forEach(([depotId, depotEvents]) => {
      const concessionCount = depotEvents.filter((event) => event.isConcession).length
      const rate = concessionCount / depotEvents.length
      if (rate > 0.08) {
        const affectedDrivers = Array.from(new Set(depotEvents.map((event) => event.driverId)))
        patterns.push({
          id: `depot-${depotId}`,
          type: "depot_spike",
          description: `Depot ${depotId} mit überdurchschnittlicher Konzessionsrate (${(rate * 100).toFixed(1)}%)`,
          severity: determineSeverity(rate + 0.02),
          confidence: Math.min(1, Math.max(0.45, rate + 0.05)),
          drivers: affectedDrivers,
          depotId,
        })
      }
    })

    const trends: TrendDetection[] = []

    Object.entries(byDriver).forEach(([driverId, driverEvents]) => {
      const sorted = driverEvents.sort((a, b) => new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime())
      const midpoint = Math.floor(sorted.length / 2)
      const firstHalf = sorted.slice(0, midpoint)
      const secondHalf = sorted.slice(midpoint)

      const firstRate =
        firstHalf.filter((event) => event.isConcession).length / (firstHalf.length || 1)
      const secondRate =
        secondHalf.filter((event) => event.isConcession).length / (secondHalf.length || 1)
      const change = secondRate - firstRate

      let direction: TrendDetection["direction"] = "stable"
      if (change > 0.02) direction = "increasing"
      else if (change < -0.02) direction = "decreasing"

      trends.push({
        driverId,
        direction,
        change: Number((change * 100).toFixed(2)),
        significance: Number(Math.abs(change * 10).toFixed(2)),
      })
    })

    return { patterns, trends }
  }
}

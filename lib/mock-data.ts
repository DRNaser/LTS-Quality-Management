// Mock data for the LTS Quality Management Platform

export interface Depot {
  id: string
  name: string
  region: string
}

export interface Driver {
  id: string
  name: string
  depotId: string
  deliveries: number
  concessions: number
  concessionRate: number
  trend: number // percentage change
  riskScore: number // 0-100
  contactRate: number
  geoMismatchRate: number
  costTotal: number
}

export interface DailyMetric {
  date: string
  deliveries: number
  concessions: number
  rate: number
  cost: number
}

export interface ConcessionType {
  type: string
  count: number
  percentage: number
}

export interface ConcessionEvent {
  id: string
  driverId: string
  depotId: string
  timestamp: string
  isConcession: boolean
  type: string
}

export interface HourlyPattern {
  hour: number
  day: string
  concessions: number
}

export interface AbusePattern {
  id: string
  address: string
  zipCode: string
  occurrences: number
  drivers: number
  severity: "critical" | "high" | "medium" | "low"
  lastOccurrence: string
  pattern: string
}

// Mock depots
export const depots: Depot[] = [
  { id: "DUS1", name: "Düsseldorf Zentrum", region: "NRW" },
  { id: "DUS2", name: "Düsseldorf Nord", region: "NRW" },
  { id: "CGN1", name: "Köln Süd", region: "NRW" },
  { id: "BER1", name: "Berlin Mitte", region: "Berlin" },
  { id: "MUC1", name: "München Ost", region: "Bayern" },
]

// Generate mock drivers
export const generateDrivers = (count = 50): Driver[] => {
  const firstNames = [
    "Max",
    "Anna",
    "Lukas",
    "Sophie",
    "Felix",
    "Emma",
    "Leon",
    "Mia",
    "Paul",
    "Lena",
    "Jonas",
    "Laura",
    "Tim",
    "Julia",
    "David",
  ]
  const lastNames = [
    "Müller",
    "Schmidt",
    "Schneider",
    "Fischer",
    "Weber",
    "Meyer",
    "Wagner",
    "Becker",
    "Hoffmann",
    "Schulz",
    "Koch",
    "Richter",
    "Klein",
    "Wolf",
    "Schröder",
  ]

  return Array.from({ length: count }, (_, i) => {
    const deliveries = Math.floor(Math.random() * 500) + 200
    const concessionRate = Math.random() * 0.15 + 0.02
    const concessions = Math.floor(deliveries * concessionRate)
    const riskScore = Math.min(100, Math.floor(concessionRate * 500 + Math.random() * 20))

    return {
      id: `DRV-${String(i + 1).padStart(4, "0")}`,
      name: `${firstNames[Math.floor(Math.random() * firstNames.length)]} ${lastNames[Math.floor(Math.random() * lastNames.length)]}`,
      depotId: depots[Math.floor(Math.random() * depots.length)].id,
      deliveries,
      concessions,
      concessionRate: Math.round(concessionRate * 10000) / 100,
      trend: Math.round((Math.random() * 4 - 2) * 100) / 100,
      riskScore,
      contactRate: Math.round((Math.random() * 0.3 + 0.6) * 100),
      geoMismatchRate: Math.round(Math.random() * 8 * 100) / 100,
      costTotal: Math.round(concessions * (Math.random() * 5 + 2) * 100) / 100,
    }
  })
}

// Generate daily metrics for the last 30 days
export const generateDailyMetrics = (days = 30): DailyMetric[] => {
  const metrics: DailyMetric[] = []
  const today = new Date()

  for (let i = days - 1; i >= 0; i--) {
    const date = new Date(today)
    date.setDate(date.getDate() - i)
    const deliveries = Math.floor(Math.random() * 2000) + 3000
    const rate = Math.random() * 0.04 + 0.04
    const concessions = Math.floor(deliveries * rate)

    metrics.push({
      date: date.toISOString().split("T")[0],
      deliveries,
      concessions,
      rate: Math.round(rate * 10000) / 100,
      cost: Math.round(concessions * 3.5 * 100) / 100,
    })
  }

  return metrics
}

// Concession type distribution
export const concessionTypes: ConcessionType[] = [
  { type: "Nachbar", count: 1245, percentage: 42 },
  { type: "Briefkasten", count: 892, percentage: 30 },
  { type: "Haushaltsmitglied", count: 534, percentage: 18 },
  { type: "Sicherer Ort", count: 297, percentage: 10 },
]

// Hourly pattern data
export const generateHourlyPatterns = (): HourlyPattern[] => {
  const days = ["Mo", "Di", "Mi", "Do", "Fr", "Sa"]
  const patterns: HourlyPattern[] = []

  for (const day of days) {
    for (let hour = 6; hour <= 21; hour++) {
      const isMorningPeak = hour >= 6 && hour <= 9
      const isEveningPeak = hour >= 17 && hour <= 20
      const baseRate = isMorningPeak ? 15 : isEveningPeak ? 12 : 5

      patterns.push({
        hour,
        day,
        concessions: Math.floor(baseRate + Math.random() * 10),
      })
    }
  }

  return patterns
}

// Abuse patterns
export const abusePatterns: AbusePattern[] = [
  {
    id: "ABP-001",
    address: "Hauptstraße 42",
    zipCode: "40210",
    occurrences: 23,
    drivers: 8,
    severity: "critical",
    lastOccurrence: "2024-01-12",
    pattern: "Wiederholt keine Annahme trotz Anwesenheit",
  },
  {
    id: "ABP-002",
    address: "Marktplatz 15",
    zipCode: "40213",
    occurrences: 18,
    drivers: 6,
    severity: "high",
    lastOccurrence: "2024-01-11",
    pattern: "Häufige Nachbar-Zustellung verlangt",
  },
  {
    id: "ABP-003",
    address: "Bergstraße 7",
    zipCode: "40215",
    occurrences: 12,
    drivers: 4,
    severity: "high",
    lastOccurrence: "2024-01-10",
    pattern: "Systematische Geo-Abweichung",
  },
  {
    id: "ABP-004",
    address: "Lindenallee 88",
    zipCode: "40211",
    occurrences: 8,
    drivers: 3,
    severity: "medium",
    lastOccurrence: "2024-01-09",
    pattern: "Unregelmäßige Kontaktverweigerung",
  },
  {
    id: "ABP-005",
    address: "Parkweg 23",
    zipCode: "40217",
    occurrences: 5,
    drivers: 2,
    severity: "low",
    lastOccurrence: "2024-01-08",
    pattern: "Gelegentliche Briefkasten-Präferenz",
  },
]

export const generateConcessionEvents = (count = 120): ConcessionEvent[] => {
  const drivers = generateDrivers(25)
  const events: ConcessionEvent[] = []
  const today = new Date()

  for (let i = 0; i < count; i++) {
    const driver = drivers[Math.floor(Math.random() * drivers.length)]
    const dayOffset = Math.floor(Math.random() * 28)
    const date = new Date(today)
    date.setDate(date.getDate() - dayOffset)

    const isConcession = Math.random() < driver.concessionRate / 100 + 0.03
    events.push({
      id: `EVT-${i + 1}`,
      driverId: driver.id,
      depotId: driver.depotId,
      timestamp: date.toISOString(),
      isConcession,
      type: isConcession ? "Nachbar" : "Standard",
    })
  }

  return events
}

// Feature importance for ML model
export const featureImportance = [
  { feature: "Kontaktrate", importance: 0.28 },
  { feature: "Geo-Abweichung", importance: 0.22 },
  { feature: "Morgenstunden-Ratio", importance: 0.18 },
  { feature: "Volatilität 60d", importance: 0.14 },
  { feature: "Hochwertige Pakete", importance: 0.1 },
  { feature: "Trend 7d", importance: 0.08 },
]

// Generate depot comparison data
export const generateDepotComparison = () => {
  return depots.map((depot) => ({
    ...depot,
    deliveries: Math.floor(Math.random() * 5000) + 8000,
    concessionRate: Math.round((Math.random() * 0.06 + 0.04) * 100) / 100,
    trend: Math.round((Math.random() * 2 - 1) * 100) / 100,
    drivers: Math.floor(Math.random() * 20) + 15,
    costPerDelivery: Math.round((Math.random() * 0.3 + 0.1) * 100) / 100,
  }))
}

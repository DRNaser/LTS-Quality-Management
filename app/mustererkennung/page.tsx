"use client"

import { useMemo } from "react"
import { Sidebar } from "@/components/dashboard/sidebar"
import { Header } from "@/components/dashboard/header"
import { KPICard } from "@/components/dashboard/kpi-card"
import { ChartCard } from "@/components/dashboard/chart-card"
import { StatusBadge } from "@/components/dashboard/status-badge"
import { generateHourlyPatterns, generateDrivers } from "@/lib/mock-data"
import { Search, Clock, MapPin, Activity, Zap } from "lucide-react"
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
} from "recharts"

// Cluster data
const clusterData = [
  {
    id: "cluster-1",
    name: "Morgenstunden-Cluster",
    description: "Hohe Konzessionsraten zwischen 6-9 Uhr",
    drivers: 12,
    avgRate: 8.5,
    severity: "high" as const,
    factors: ["Zeitdruck", "Wenig Personal", "Rush Hour"],
  },
  {
    id: "cluster-2",
    name: "Geo-Abweichungs-Cluster",
    description: "Systematische GPS-Abweichungen > 25m",
    drivers: 8,
    avgRate: 7.2,
    severity: "high" as const,
    factors: ["Falsche Adressen", "GPS-Probleme", "Abkürzungen"],
  },
  {
    id: "cluster-3",
    name: "Kontaktvermeidungs-Cluster",
    description: "Niedrige Kontaktrate bei hoher Lieferzahl",
    drivers: 15,
    avgRate: 6.1,
    severity: "medium" as const,
    factors: ["Zeiteffizienz", "Kundenabwesenheit", "Training"],
  },
  {
    id: "cluster-4",
    name: "Hochwertige-Pakete-Cluster",
    description: "Erhöhte Konzessionen bei High-Value Items",
    drivers: 6,
    avgRate: 5.8,
    severity: "medium" as const,
    factors: ["Sicherheitsbedenken", "Unterschrift erforderlich"],
  },
]

// Anomalies detected
const anomalies = [
  {
    id: "anom-1",
    type: "Zeitliches Muster",
    description: "Ungewöhnlich hohe Konzessionsrate am Montag früh",
    deviation: "+45%",
    severity: "critical" as const,
  },
  {
    id: "anom-2",
    type: "Geographisch",
    description: "PLZ 40210: 3x höhere Rate als Durchschnitt",
    deviation: "+210%",
    severity: "critical" as const,
  },
  {
    id: "anom-3",
    type: "Fahrer-Gruppe",
    description: "5 Fahrer mit identischem Muster in Depot DUS1",
    deviation: "+85%",
    severity: "high" as const,
  },
  {
    id: "anom-4",
    type: "Saisonal",
    description: "Anstieg im Dezember über Erwartung",
    deviation: "+22%",
    severity: "medium" as const,
  },
]

// Correlation data
const correlationData = [
  { factor: "Kontaktrate", correlation: -0.72 },
  { factor: "Geo-Abweichung", correlation: 0.68 },
  { factor: "Lieferzeit", correlation: 0.45 },
  { factor: "Paketgewicht", correlation: 0.23 },
  { factor: "Erfahrung (Jahre)", correlation: -0.31 },
  { factor: "Routen-Effizienz", correlation: -0.42 },
]

export default function PatternRecognitionPage() {
  const hourlyPatterns = useMemo(() => generateHourlyPatterns(), [])
  const drivers = useMemo(() => generateDrivers(50), [])

  // Create heatmap data structure
  const heatmapData = useMemo(() => {
    const days = ["Mo", "Di", "Mi", "Do", "Fr", "Sa"]
    const hours = Array.from({ length: 16 }, (_, i) => i + 6)

    return days.map((day) => ({
      day,
      ...Object.fromEntries(
        hours.map((hour) => {
          const pattern = hourlyPatterns.find((p) => p.day === day && p.hour === hour)
          return [`h${hour}`, pattern?.concessions || 0]
        }),
      ),
    }))
  }, [hourlyPatterns])

  // Radar chart data for pattern comparison
  const radarData = [
    { subject: "Morgen", A: 85, B: 45, fullMark: 100 },
    { subject: "Vormittag", A: 60, B: 70, fullMark: 100 },
    { subject: "Mittag", A: 45, B: 55, fullMark: 100 },
    { subject: "Nachmittag", A: 55, B: 65, fullMark: 100 },
    { subject: "Abend", A: 75, B: 40, fullMark: 100 },
    { subject: "Spät", A: 35, B: 30, fullMark: 100 },
  ]

  const getSeverityStatus = (severity: string): "success" | "warning" | "danger" => {
    if (severity === "critical" || severity === "high") return "danger"
    if (severity === "medium") return "warning"
    return "success"
  }

  return (
    <div className="flex min-h-screen">
      <Sidebar />
      <main className="ml-64 flex-1">
        <Header title="Mustererkennung" subtitle="Automatische Pattern-Analyse und Clustering" />

        <div className="p-6">
          {/* KPI Row */}
          <div className="mb-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            <KPICard
              title="Erkannte Cluster"
              value={clusterData.length}
              subtitle="Aktive Mustergruppen"
              icon={Search}
            />
            <KPICard
              title="Anomalien"
              value={anomalies.length}
              subtitle={`${anomalies.filter((a) => a.severity === "critical").length} kritisch`}
              icon={Zap}
              variant="warning"
            />
            <KPICard
              title="Peak-Stunde"
              value="07:00"
              subtitle="Höchste Konzessionsrate"
              icon={Clock}
              variant="danger"
            />
            <KPICard
              title="Betroffene PLZ"
              value="23"
              subtitle="Mit auffälligen Mustern"
              icon={MapPin}
              variant="warning"
            />
          </div>

          {/* Heatmap */}
          <div className="mb-6">
            <ChartCard title="Stündliche Konzessions-Heatmap" subtitle="Konzessionen nach Wochentag und Uhrzeit">
              <div className="overflow-x-auto">
                <div className="min-w-[800px]">
                  {/* Hour labels */}
                  <div className="flex mb-2 ml-12">
                    {Array.from({ length: 16 }, (_, i) => i + 6).map((hour) => (
                      <div key={hour} className="flex-1 text-center text-xs text-muted-foreground">
                        {hour}:00
                      </div>
                    ))}
                  </div>
                  {/* Heatmap rows */}
                  {heatmapData.map((row) => (
                    <div key={row.day} className="flex items-center mb-1">
                      <div className="w-12 text-sm text-muted-foreground">{row.day}</div>
                      <div className="flex flex-1 gap-1">
                        {Array.from({ length: 16 }, (_, i) => i + 6).map((hour) => {
                          const value = row[`h${hour}` as keyof typeof row] as number
                          const intensity = Math.min(1, value / 25)
                          return (
                            <div
                              key={hour}
                              className="flex-1 h-8 rounded-sm flex items-center justify-center text-xs font-medium transition-colors hover:ring-1 hover:ring-primary cursor-pointer"
                              style={{
                                backgroundColor: `rgba(99, 102, 241, ${intensity})`,
                                color: intensity > 0.5 ? "white" : "inherit",
                              }}
                              title={`${row.day} ${hour}:00 - ${value} Konzessionen`}
                            >
                              {value > 10 ? value : ""}
                            </div>
                          )
                        })}
                      </div>
                    </div>
                  ))}
                  {/* Legend */}
                  <div className="flex items-center justify-end gap-2 mt-4">
                    <span className="text-xs text-muted-foreground">Wenig</span>
                    <div className="flex gap-0.5">
                      {[0.1, 0.3, 0.5, 0.7, 0.9].map((intensity) => (
                        <div
                          key={intensity}
                          className="h-4 w-6 rounded-sm"
                          style={{ backgroundColor: `rgba(99, 102, 241, ${intensity})` }}
                        />
                      ))}
                    </div>
                    <span className="text-xs text-muted-foreground">Viel</span>
                  </div>
                </div>
              </div>
            </ChartCard>
          </div>

          {/* Clusters and Anomalies */}
          <div className="mb-6 grid gap-6 lg:grid-cols-2">
            {/* Clusters */}
            <ChartCard title="Erkannte Cluster" subtitle="Automatisch gruppierte Muster">
              <div className="space-y-3">
                {clusterData.map((cluster) => (
                  <div
                    key={cluster.id}
                    className="rounded-lg border border-border bg-secondary/30 p-4 hover:bg-secondary/50 transition-colors cursor-pointer"
                  >
                    <div className="flex items-start justify-between mb-2">
                      <div>
                        <h4 className="font-medium text-foreground">{cluster.name}</h4>
                        <p className="text-sm text-muted-foreground">{cluster.description}</p>
                      </div>
                      <StatusBadge
                        status={getSeverityStatus(cluster.severity)}
                        label={cluster.severity === "high" ? "Hoch" : "Mittel"}
                      />
                    </div>
                    <div className="flex items-center gap-4 text-sm">
                      <span className="text-muted-foreground">
                        <strong className="text-foreground">{cluster.drivers}</strong> Fahrer
                      </span>
                      <span className="text-muted-foreground">
                        <strong className="text-foreground">{cluster.avgRate}%</strong> Avg. Rate
                      </span>
                    </div>
                    <div className="mt-2 flex flex-wrap gap-1">
                      {cluster.factors.map((factor) => (
                        <span
                          key={factor}
                          className="inline-flex items-center rounded-full bg-primary/10 px-2 py-0.5 text-xs text-primary"
                        >
                          {factor}
                        </span>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </ChartCard>

            {/* Anomalies */}
            <ChartCard title="Anomalien" subtitle="Abweichungen vom erwarteten Muster">
              <div className="space-y-3">
                {anomalies.map((anomaly) => (
                  <div
                    key={anomaly.id}
                    className="rounded-lg border border-border bg-secondary/30 p-4 hover:bg-secondary/50 transition-colors cursor-pointer"
                  >
                    <div className="flex items-start justify-between">
                      <div>
                        <div className="flex items-center gap-2 mb-1">
                          <Activity className="h-4 w-4 text-primary" />
                          <span className="text-xs font-medium text-primary">{anomaly.type}</span>
                        </div>
                        <p className="text-sm text-foreground">{anomaly.description}</p>
                      </div>
                      <div className="text-right">
                        <StatusBadge
                          status={getSeverityStatus(anomaly.severity)}
                          label={
                            anomaly.severity === "critical"
                              ? "Kritisch"
                              : anomaly.severity === "high"
                                ? "Hoch"
                                : "Mittel"
                          }
                        />
                        <p className="mt-1 text-sm font-bold text-destructive">{anomaly.deviation}</p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </ChartCard>
          </div>

          {/* Correlations and Radar */}
          <div className="grid gap-6 lg:grid-cols-2">
            {/* Correlation Analysis */}
            <ChartCard title="Korrelationsanalyse" subtitle="Faktoren und ihre Auswirkung auf die Konzessionsrate">
              <div className="h-64">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={correlationData} layout="vertical">
                    <CartesianGrid strokeDasharray="3 3" stroke="#333" horizontal={false} />
                    <XAxis type="number" stroke="#666" fontSize={10} domain={[-1, 1]} />
                    <YAxis type="category" dataKey="factor" stroke="#666" fontSize={10} width={120} />
                    <Tooltip
                      contentStyle={{ backgroundColor: "#1a1a2e", border: "1px solid #333", borderRadius: "8px" }}
                      formatter={(value: number) => [value.toFixed(2), "Korrelation"]}
                    />
                    <Bar dataKey="correlation" radius={[0, 4, 4, 0]}>
                      {correlationData.map((entry, index) => (
                        <Bar
                          key={`cell-${index}`}
                          dataKey="correlation"
                          fill={entry.correlation > 0 ? "#ef4444" : "#22c55e"}
                        />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </div>
              <div className="mt-4 flex items-center justify-center gap-6 text-xs">
                <div className="flex items-center gap-2">
                  <div className="h-3 w-3 rounded-full bg-success" />
                  <span className="text-muted-foreground">Negativ (reduziert Rate)</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="h-3 w-3 rounded-full bg-destructive" />
                  <span className="text-muted-foreground">Positiv (erhöht Rate)</span>
                </div>
              </div>
            </ChartCard>

            {/* Pattern Comparison Radar */}
            <ChartCard title="Muster-Vergleich" subtitle="Hochrisiko vs. Normalfahrer">
              <div className="h-64">
                <ResponsiveContainer width="100%" height="100%">
                  <RadarChart data={radarData}>
                    <PolarGrid stroke="#333" />
                    <PolarAngleAxis dataKey="subject" stroke="#666" fontSize={10} />
                    <PolarRadiusAxis stroke="#666" fontSize={8} />
                    <Radar name="Hochrisiko" dataKey="A" stroke="#ef4444" fill="#ef4444" fillOpacity={0.3} />
                    <Radar name="Normal" dataKey="B" stroke="#22c55e" fill="#22c55e" fillOpacity={0.3} />
                    <Tooltip
                      contentStyle={{ backgroundColor: "#1a1a2e", border: "1px solid #333", borderRadius: "8px" }}
                    />
                  </RadarChart>
                </ResponsiveContainer>
              </div>
              <div className="mt-4 flex items-center justify-center gap-6 text-xs">
                <div className="flex items-center gap-2">
                  <div className="h-3 w-3 rounded-full bg-destructive" />
                  <span className="text-muted-foreground">Hochrisiko-Fahrer</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="h-3 w-3 rounded-full bg-success" />
                  <span className="text-muted-foreground">Normal-Fahrer</span>
                </div>
              </div>
            </ChartCard>
          </div>
        </div>
      </main>
    </div>
  )
}

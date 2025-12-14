"use client"

import { useMemo, useState } from "react"
import { Sidebar } from "@/components/dashboard/sidebar"
import { Header } from "@/components/dashboard/header"
import { KPICard } from "@/components/dashboard/kpi-card"
import { ChartCard } from "@/components/dashboard/chart-card"
import { DataTable } from "@/components/dashboard/data-table"
import { StatusBadge } from "@/components/dashboard/status-badge"
import { generateDrivers, featureImportance, depots } from "@/lib/mock-data"
import { Target, AlertTriangle, Users, TrendingUp, Download, Filter } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  ScatterChart,
  Scatter,
  ZAxis,
} from "recharts"

const RISK_COLORS = {
  high: "#ef4444",
  medium: "#f59e0b",
  low: "#22c55e",
}

export default function RiskAnalysisPage() {
  const [selectedDepot, setSelectedDepot] = useState<string>("all")
  const allDrivers = useMemo(() => generateDrivers(100), [])

  const drivers = useMemo(() => {
    if (selectedDepot === "all") return allDrivers
    return allDrivers.filter((d) => d.depotId === selectedDepot)
  }, [allDrivers, selectedDepot])

  // Risk distribution
  const riskDistribution = useMemo(() => {
    const high = drivers.filter((d) => d.riskScore >= 70).length
    const medium = drivers.filter((d) => d.riskScore >= 40 && d.riskScore < 70).length
    const low = drivers.filter((d) => d.riskScore < 40).length
    return [
      { name: "Hoch (70-100)", value: high, color: RISK_COLORS.high },
      { name: "Mittel (40-69)", value: medium, color: RISK_COLORS.medium },
      { name: "Niedrig (0-39)", value: low, color: RISK_COLORS.low },
    ]
  }, [drivers])

  const highRiskDrivers = useMemo(
    () => drivers.filter((d) => d.riskScore >= 70).sort((a, b) => b.riskScore - a.riskScore),
    [drivers],
  )

  const avgRiskScore = Math.round(drivers.reduce((sum, d) => sum + d.riskScore, 0) / drivers.length)

  // Scatter plot data for risk vs concession rate
  const scatterData = useMemo(
    () =>
      drivers.map((d) => ({
        x: d.concessionRate,
        y: d.riskScore,
        z: d.deliveries,
        name: d.name,
        id: d.id,
      })),
    [drivers],
  )

  const getRiskStatus = (score: number): "success" | "warning" | "danger" => {
    if (score >= 70) return "danger"
    if (score >= 40) return "warning"
    return "success"
  }

  const driverColumns = [
    { key: "name", header: "Fahrer" },
    { key: "id", header: "ID", className: "text-muted-foreground font-mono text-xs" },
    { key: "depotId", header: "Depot" },
    {
      key: "riskScore",
      header: "Risiko-Score",
      render: (d: (typeof drivers)[0]) => (
        <div className="flex items-center gap-2">
          <div className="h-2 w-16 rounded-full bg-secondary overflow-hidden">
            <div
              className="h-full rounded-full transition-all"
              style={{
                width: `${d.riskScore}%`,
                backgroundColor:
                  d.riskScore >= 70 ? RISK_COLORS.high : d.riskScore >= 40 ? RISK_COLORS.medium : RISK_COLORS.low,
              }}
            />
          </div>
          <span className="font-medium">{d.riskScore}</span>
        </div>
      ),
    },
    {
      key: "concessionRate",
      header: "Konzessionsrate",
      render: (d: (typeof drivers)[0]) => `${d.concessionRate.toFixed(2)}%`,
    },
    {
      key: "contactRate",
      header: "Kontaktrate",
      render: (d: (typeof drivers)[0]) => `${d.contactRate}%`,
    },
    {
      key: "geoMismatchRate",
      header: "Geo-Abweichung",
      render: (d: (typeof drivers)[0]) => `${d.geoMismatchRate.toFixed(2)}%`,
    },
    {
      key: "status",
      header: "Status",
      render: (d: (typeof drivers)[0]) => (
        <StatusBadge
          status={getRiskStatus(d.riskScore)}
          label={d.riskScore >= 70 ? "Kritisch" : d.riskScore >= 40 ? "Beobachten" : "OK"}
        />
      ),
    },
  ]

  return (
    <div className="flex min-h-screen">
      <Sidebar />
      <main className="ml-64 flex-1">
        <Header title="Risikoanalyse" subtitle="ML-basierte Fahrerbewertung" />

        <div className="p-6">
          {/* Filters */}
          <div className="mb-6 flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-2">
                <Filter className="h-4 w-4 text-muted-foreground" />
                <Select value={selectedDepot} onValueChange={setSelectedDepot}>
                  <SelectTrigger className="w-[200px] border-border bg-secondary">
                    <SelectValue placeholder="Depot wählen" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">Alle Depots</SelectItem>
                    {depots.map((depot) => (
                      <SelectItem key={depot.id} value={depot.id}>
                        {depot.name}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </div>
            <Button variant="outline" size="sm" className="gap-2 bg-transparent">
              <Download className="h-4 w-4" />
              Export Coaching-Liste
            </Button>
          </div>

          {/* KPI Row */}
          <div className="mb-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            <KPICard
              title="Durchschnittlicher Risiko-Score"
              value={avgRiskScore}
              subtitle="Von 100"
              icon={Target}
              variant={avgRiskScore >= 50 ? "warning" : "success"}
            />
            <KPICard
              title="Hochrisiko-Fahrer"
              value={highRiskDrivers.length}
              subtitle={`${((highRiskDrivers.length / drivers.length) * 100).toFixed(1)}% aller Fahrer`}
              icon={AlertTriangle}
              variant="danger"
            />
            <KPICard
              title="Analysierte Fahrer"
              value={drivers.length}
              subtitle={selectedDepot === "all" ? "Alle Depots" : `Depot: ${selectedDepot}`}
              icon={Users}
            />
            <KPICard
              title="Trend-Warnung"
              value={drivers.filter((d) => d.trend > 1).length}
              subtitle="Fahrer mit steigender Rate"
              icon={TrendingUp}
              variant="warning"
            />
          </div>

          {/* Charts Row */}
          <div className="mb-6 grid gap-6 lg:grid-cols-3">
            {/* Risk Distribution Pie Chart */}
            <ChartCard title="Risiko-Verteilung" subtitle="Nach Risiko-Kategorie">
              <div className="h-64 flex items-center">
                <ResponsiveContainer width="60%" height="100%">
                  <PieChart>
                    <Pie
                      data={riskDistribution}
                      cx="50%"
                      cy="50%"
                      innerRadius={40}
                      outerRadius={70}
                      paddingAngle={2}
                      dataKey="value"
                    >
                      {riskDistribution.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip
                      contentStyle={{ backgroundColor: "#1a1a2e", border: "1px solid #333", borderRadius: "8px" }}
                      formatter={(value: number) => [value, "Fahrer"]}
                    />
                  </PieChart>
                </ResponsiveContainer>
                <div className="flex-1 space-y-3">
                  {riskDistribution.map((item) => (
                    <div key={item.name} className="flex items-center gap-2">
                      <div className="h-3 w-3 rounded-full" style={{ backgroundColor: item.color }} />
                      <div className="flex-1">
                        <p className="text-sm text-muted-foreground">{item.name}</p>
                        <p className="text-lg font-semibold">{item.value}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </ChartCard>

            {/* Feature Importance */}
            <ChartCard title="Feature-Wichtigkeit" subtitle="ML-Modell Einflussfaktoren">
              <div className="h-64">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={featureImportance} layout="vertical">
                    <CartesianGrid strokeDasharray="3 3" stroke="#333" horizontal={false} />
                    <XAxis
                      type="number"
                      stroke="#666"
                      fontSize={10}
                      tickFormatter={(v) => `${(v * 100).toFixed(0)}%`}
                    />
                    <YAxis type="category" dataKey="feature" stroke="#666" fontSize={10} width={100} />
                    <Tooltip
                      contentStyle={{ backgroundColor: "#1a1a2e", border: "1px solid #333", borderRadius: "8px" }}
                      formatter={(value: number) => [`${(value * 100).toFixed(1)}%`, "Wichtigkeit"]}
                    />
                    <Bar dataKey="importance" fill="#6366f1" radius={[0, 4, 4, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </ChartCard>

            {/* Scatter Plot */}
            <ChartCard title="Risiko vs. Konzessionsrate" subtitle="Korrelationsanalyse">
              <div className="h-64">
                <ResponsiveContainer width="100%" height="100%">
                  <ScatterChart>
                    <CartesianGrid strokeDasharray="3 3" stroke="#333" />
                    <XAxis
                      type="number"
                      dataKey="x"
                      stroke="#666"
                      fontSize={10}
                      name="Konzessionsrate"
                      tickFormatter={(v) => `${v}%`}
                    />
                    <YAxis
                      type="number"
                      dataKey="y"
                      stroke="#666"
                      fontSize={10}
                      name="Risiko-Score"
                      domain={[0, 100]}
                    />
                    <ZAxis type="number" dataKey="z" range={[20, 200]} name="Lieferungen" />
                    <Tooltip
                      contentStyle={{ backgroundColor: "#1a1a2e", border: "1px solid #333", borderRadius: "8px" }}
                      formatter={(value: number, name: string) => {
                        if (name === "Konzessionsrate") return [`${value.toFixed(2)}%`, name]
                        return [value, name]
                      }}
                      cursor={{ strokeDasharray: "3 3" }}
                    />
                    <Scatter name="Fahrer" data={scatterData} fill="#6366f1">
                      {scatterData.map((entry, index) => (
                        <Cell
                          key={`cell-${index}`}
                          fill={entry.y >= 70 ? RISK_COLORS.high : entry.y >= 40 ? RISK_COLORS.medium : RISK_COLORS.low}
                        />
                      ))}
                    </Scatter>
                  </ScatterChart>
                </ResponsiveContainer>
              </div>
            </ChartCard>
          </div>

          {/* Risk Score Gauge */}
          <div className="mb-6">
            <ChartCard title="Gesamt-Risikobewertung" subtitle="Aggregierter Score aller Fahrer">
              <div className="flex items-center justify-center py-8">
                <div className="relative h-40 w-40">
                  <svg className="h-full w-full -rotate-90" viewBox="0 0 100 100">
                    {/* Background circle */}
                    <circle
                      cx="50"
                      cy="50"
                      r="40"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="8"
                      className="text-secondary"
                    />
                    {/* Progress circle */}
                    <circle
                      cx="50"
                      cy="50"
                      r="40"
                      fill="none"
                      stroke={
                        avgRiskScore >= 70
                          ? RISK_COLORS.high
                          : avgRiskScore >= 40
                            ? RISK_COLORS.medium
                            : RISK_COLORS.low
                      }
                      strokeWidth="8"
                      strokeLinecap="round"
                      strokeDasharray={`${avgRiskScore * 2.51} 251`}
                    />
                  </svg>
                  <div className="absolute inset-0 flex flex-col items-center justify-center">
                    <span className="text-3xl font-bold">{avgRiskScore}</span>
                    <span className="text-xs text-muted-foreground">von 100</span>
                  </div>
                </div>
                <div className="ml-8 space-y-4">
                  <div className="flex items-center gap-3">
                    <div className="h-3 w-3 rounded-full" style={{ backgroundColor: RISK_COLORS.low }} />
                    <div>
                      <p className="text-sm font-medium">Niedriges Risiko (0-39)</p>
                      <p className="text-xs text-muted-foreground">Keine Maßnahmen erforderlich</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-3">
                    <div className="h-3 w-3 rounded-full" style={{ backgroundColor: RISK_COLORS.medium }} />
                    <div>
                      <p className="text-sm font-medium">Mittleres Risiko (40-69)</p>
                      <p className="text-xs text-muted-foreground">Beobachtung empfohlen</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-3">
                    <div className="h-3 w-3 rounded-full" style={{ backgroundColor: RISK_COLORS.high }} />
                    <div>
                      <p className="text-sm font-medium">Hohes Risiko (70-100)</p>
                      <p className="text-xs text-muted-foreground">Sofortiges Coaching erforderlich</p>
                    </div>
                  </div>
                </div>
              </div>
            </ChartCard>
          </div>

          {/* Driver Table */}
          <ChartCard
            title="Fahrer-Risikobewertung"
            subtitle={`${highRiskDrivers.length} Fahrer mit hohem Risiko`}
            action={
              <StatusBadge
                status={highRiskDrivers.length > 10 ? "danger" : highRiskDrivers.length > 5 ? "warning" : "success"}
                label={`${highRiskDrivers.length} kritisch`}
              />
            }
          >
            <DataTable
              data={highRiskDrivers.slice(0, 10)}
              columns={driverColumns}
              onRowClick={(driver) => console.log("Navigate to driver:", driver.id)}
            />
            {highRiskDrivers.length > 10 && (
              <div className="mt-4 text-center">
                <Button variant="outline" size="sm">
                  Alle {highRiskDrivers.length} Fahrer anzeigen
                </Button>
              </div>
            )}
          </ChartCard>
        </div>
      </main>
    </div>
  )
}

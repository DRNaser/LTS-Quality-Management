"use client"

import { useMemo } from "react"
import { Sidebar } from "@/components/dashboard/sidebar"
import { Header } from "@/components/dashboard/header"
import { KPICard } from "@/components/dashboard/kpi-card"
import { ChartCard } from "@/components/dashboard/chart-card"
import { DataTable } from "@/components/dashboard/data-table"
import { StatusBadge } from "@/components/dashboard/status-badge"
import { generateDepotComparison, generateDailyMetrics } from "@/lib/mock-data"
import { Building2, TrendingUp, TrendingDown, Euro } from "lucide-react"
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  LineChart,
  Line,
  Legend,
} from "recharts"

const DEPOT_COLORS: Record<string, string> = {
  DUS1: "#6366f1",
  DUS2: "#22c55e",
  CGN1: "#f59e0b",
  BER1: "#ef4444",
  MUC1: "#8b5cf6",
}

export default function DepotComparisonPage() {
  const depotData = useMemo(() => generateDepotComparison(), [])
  const dailyMetrics = useMemo(() => generateDailyMetrics(14), [])

  // Generate weekly data per depot
  const weeklyDepotData = useMemo(() => {
    const weeks = ["KW 49", "KW 50", "KW 51", "KW 52"]
    return weeks.map((week) => ({
      week,
      DUS1: Math.round((Math.random() * 0.04 + 0.04) * 100) / 100,
      DUS2: Math.round((Math.random() * 0.04 + 0.04) * 100) / 100,
      CGN1: Math.round((Math.random() * 0.04 + 0.04) * 100) / 100,
      BER1: Math.round((Math.random() * 0.04 + 0.04) * 100) / 100,
      MUC1: Math.round((Math.random() * 0.04 + 0.04) * 100) / 100,
    }))
  }, [])

  const bestDepot = depotData.reduce((best, depot) => (depot.concessionRate < best.concessionRate ? depot : best))
  const worstDepot = depotData.reduce((worst, depot) => (depot.concessionRate > worst.concessionRate ? depot : worst))

  const avgRate = depotData.reduce((sum, d) => sum + d.concessionRate, 0) / depotData.length
  const totalDeliveries = depotData.reduce((sum, d) => sum + d.deliveries, 0)

  const getRateStatus = (rate: number): "success" | "warning" | "danger" => {
    if (rate <= 0.05) return "success"
    if (rate <= 0.07) return "warning"
    return "danger"
  }

  const depotColumns = [
    { key: "name", header: "Depot" },
    { key: "region", header: "Region", className: "text-muted-foreground" },
    {
      key: "deliveries",
      header: "Lieferungen",
      render: (d: (typeof depotData)[0]) => d.deliveries.toLocaleString("de-DE"),
    },
    { key: "drivers", header: "Fahrer" },
    {
      key: "concessionRate",
      header: "Konzessionsrate",
      render: (d: (typeof depotData)[0]) => (
        <StatusBadge status={getRateStatus(d.concessionRate)} label={`${(d.concessionRate * 100).toFixed(2)}%`} />
      ),
    },
    {
      key: "trend",
      header: "Trend",
      render: (d: (typeof depotData)[0]) => (
        <span className={d.trend > 0 ? "text-destructive" : "text-success"}>
          {d.trend > 0 ? "+" : ""}
          {d.trend.toFixed(2)}%
        </span>
      ),
    },
    {
      key: "costPerDelivery",
      header: "Kosten/Lieferung",
      render: (d: (typeof depotData)[0]) => `€${d.costPerDelivery.toFixed(2)}`,
    },
  ]

  return (
    <div className="flex min-h-screen">
      <Sidebar />
      <main className="ml-64 flex-1">
        <Header title="Depot-Vergleich" subtitle="Vergleichsanalyse aller Standorte" />

        <div className="p-6">
          {/* KPI Row */}
          <div className="mb-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            <KPICard
              title="Durchschnittliche Rate"
              value={`${(avgRate * 100).toFixed(2)}%`}
              subtitle="Alle Depots"
              icon={Building2}
            />
            <KPICard
              title="Bestes Depot"
              value={bestDepot.name}
              subtitle={`${(bestDepot.concessionRate * 100).toFixed(2)}% Rate`}
              icon={TrendingDown}
              variant="success"
            />
            <KPICard
              title="Verbesserungspotenzial"
              value={worstDepot.name}
              subtitle={`${(worstDepot.concessionRate * 100).toFixed(2)}% Rate`}
              icon={TrendingUp}
              variant="warning"
            />
            <KPICard
              title="Gesamtlieferungen"
              value={totalDeliveries.toLocaleString("de-DE")}
              subtitle="Diese Woche"
              icon={Euro}
            />
          </div>

          {/* Charts Row */}
          <div className="mb-6 grid gap-6 lg:grid-cols-2">
            <ChartCard title="Konzessionsraten nach Depot" subtitle="Aktueller Stand">
              <div className="h-64">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={depotData} layout="vertical">
                    <CartesianGrid strokeDasharray="3 3" stroke="#333" horizontal={false} />
                    <XAxis
                      type="number"
                      stroke="#666"
                      fontSize={10}
                      tickFormatter={(v) => `${(v * 100).toFixed(0)}%`}
                    />
                    <YAxis type="category" dataKey="id" stroke="#666" fontSize={10} width={50} />
                    <Tooltip
                      contentStyle={{ backgroundColor: "#1a1a2e", border: "1px solid #333", borderRadius: "8px" }}
                      formatter={(value: number) => [`${(value * 100).toFixed(2)}%`, "Rate"]}
                    />
                    <Bar dataKey="concessionRate" radius={[0, 4, 4, 0]}>
                      {depotData.map((entry) => (
                        <Bar key={entry.id} dataKey="concessionRate" fill={DEPOT_COLORS[entry.id] || "#6366f1"} />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </ChartCard>

            <ChartCard title="Wöchentlicher Trend" subtitle="Letzte 4 Wochen">
              <div className="h-64">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={weeklyDepotData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#333" />
                    <XAxis dataKey="week" stroke="#666" fontSize={10} />
                    <YAxis stroke="#666" fontSize={10} tickFormatter={(v) => `${(v * 100).toFixed(0)}%`} />
                    <Tooltip
                      contentStyle={{ backgroundColor: "#1a1a2e", border: "1px solid #333", borderRadius: "8px" }}
                      formatter={(value: number) => [`${(value * 100).toFixed(2)}%`]}
                    />
                    <Legend verticalAlign="top" height={36} />
                    {Object.keys(DEPOT_COLORS).map((depotId) => (
                      <Line
                        key={depotId}
                        type="monotone"
                        dataKey={depotId}
                        stroke={DEPOT_COLORS[depotId]}
                        strokeWidth={2}
                        dot={false}
                      />
                    ))}
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </ChartCard>
          </div>

          {/* Box Plot Simulation - Distribution */}
          <div className="mb-6">
            <ChartCard title="Fahrer-Verteilung nach Depot" subtitle="Konzessionsraten-Spanne">
              <div className="grid gap-4 py-4">
                {depotData.map((depot) => {
                  const min = Math.max(0, depot.concessionRate - 0.03)
                  const max = depot.concessionRate + 0.04
                  const q1 = depot.concessionRate - 0.01
                  const q3 = depot.concessionRate + 0.02
                  const median = depot.concessionRate

                  return (
                    <div key={depot.id} className="flex items-center gap-4">
                      <div className="w-24 text-sm text-muted-foreground">{depot.id}</div>
                      <div className="relative flex-1 h-8">
                        <div className="absolute inset-y-2 left-0 right-0 bg-secondary rounded" />
                        {/* Whiskers */}
                        <div
                          className="absolute top-3 h-2 w-px bg-muted-foreground"
                          style={{ left: `${min * 500}%` }}
                        />
                        <div
                          className="absolute top-3 h-2 w-px bg-muted-foreground"
                          style={{ left: `${max * 500}%` }}
                        />
                        {/* Line between whiskers */}
                        <div
                          className="absolute top-[14px] h-px bg-muted-foreground"
                          style={{ left: `${min * 500}%`, width: `${(max - min) * 500}%` }}
                        />
                        {/* Box */}
                        <div
                          className="absolute top-1 h-6 rounded"
                          style={{
                            left: `${q1 * 500}%`,
                            width: `${(q3 - q1) * 500}%`,
                            backgroundColor: DEPOT_COLORS[depot.id],
                            opacity: 0.6,
                          }}
                        />
                        {/* Median */}
                        <div
                          className="absolute top-1 h-6 w-0.5 rounded"
                          style={{ left: `${median * 500}%`, backgroundColor: DEPOT_COLORS[depot.id] }}
                        />
                      </div>
                      <div className="w-20 text-right text-sm font-medium">
                        {(depot.concessionRate * 100).toFixed(2)}%
                      </div>
                    </div>
                  )
                })}
              </div>
              <div className="flex justify-between text-xs text-muted-foreground px-28 mt-2">
                <span>0%</span>
                <span>5%</span>
                <span>10%</span>
                <span>15%</span>
                <span>20%</span>
              </div>
            </ChartCard>
          </div>

          {/* Depot Table */}
          <ChartCard title="Depot-Details" subtitle="Vollständige Übersicht aller Standorte">
            <DataTable
              data={depotData}
              columns={depotColumns}
              onRowClick={(depot) => console.log("Navigate to depot:", depot.id)}
            />
          </ChartCard>
        </div>
      </main>
    </div>
  )
}

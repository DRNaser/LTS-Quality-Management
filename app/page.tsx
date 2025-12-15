"use client"

import { useMemo } from "react"
import { Sidebar } from "@/components/dashboard/sidebar"
import { Header } from "@/components/dashboard/header"
import { KPICard } from "@/components/dashboard/kpi-card"
import { ChartCard } from "@/components/dashboard/chart-card"
import { DataTable } from "@/components/dashboard/data-table"
import { StatusBadge } from "@/components/dashboard/status-badge"
import { PatternsPanel } from "@/components/dashboard/patterns-panel"
import { generateDrivers, generateDailyMetrics, concessionTypes } from "@/lib/mock-data"
import { Package, Users, TrendingDown, Euro, Target } from "lucide-react"
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from "recharts"

const CHART_COLORS = ["#6366f1", "#22c55e", "#f59e0b", "#ef4444", "#8b5cf6"]

export default function OverviewPage() {
  const drivers = useMemo(() => generateDrivers(50), [])
  const dailyMetrics = useMemo(() => generateDailyMetrics(30), [])

  const totalDeliveries = dailyMetrics.reduce((sum, d) => sum + d.deliveries, 0)
  const totalConcessions = dailyMetrics.reduce((sum, d) => sum + d.concessions, 0)
  const avgRate = ((totalConcessions / totalDeliveries) * 100).toFixed(2)
  const totalCost = dailyMetrics.reduce((sum, d) => sum + d.cost, 0)

  const highRiskDrivers = drivers
    .filter((d) => d.riskScore >= 70)
    .sort((a, b) => b.riskScore - a.riskScore)
    .slice(0, 5)

  const topPerformers = drivers
    .filter((d) => d.riskScore < 30)
    .sort((a, b) => a.concessionRate - b.concessionRate)
    .slice(0, 5)

  const getRiskStatus = (score: number): "success" | "warning" | "danger" => {
    if (score >= 70) return "danger"
    if (score >= 40) return "warning"
    return "success"
  }

  const driverColumns = [
    { key: "name", header: "Fahrer" },
    { key: "depotId", header: "Depot", className: "text-muted-foreground" },
    {
      key: "concessionRate",
      header: "Konzessionsrate",
      render: (d: (typeof drivers)[0]) => `${d.concessionRate.toFixed(2)}%`,
    },
    {
      key: "trend",
      header: "Trend",
      render: (d: (typeof drivers)[0]) => (
        <span className={d.trend > 0 ? "text-destructive" : "text-success"}>
          {d.trend > 0 ? "+" : ""}
          {d.trend.toFixed(2)}%
        </span>
      ),
    },
    {
      key: "riskScore",
      header: "Risiko",
      render: (d: (typeof drivers)[0]) => <StatusBadge status={getRiskStatus(d.riskScore)} label={`${d.riskScore}`} />,
    },
  ]

  return (
    <div className="flex min-h-screen">
      <Sidebar />
      <main className="ml-64 flex-1">
        <Header title="Überblick" subtitle="Tägliche Qualitätsübersicht" />

        <div className="p-6">
          {/* KPI Row */}
          <div className="mb-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-5">
            <KPICard
              title="Lieferungen gesamt"
              value={totalDeliveries.toLocaleString("de-DE")}
              subtitle="Letzte 30 Tage"
              icon={Package}
            />
            <KPICard
              title="Aktive Fahrer"
              value={drivers.length}
              subtitle={`${highRiskDrivers.length} mit hohem Risiko`}
              icon={Users}
              variant={highRiskDrivers.length > 5 ? "warning" : "default"}
            />
            <KPICard
              title="Konzessionsrate"
              value={`${avgRate}%`}
              trend={-0.32}
              trendLabel="vs. Vorwoche"
              icon={Target}
              variant="success"
            />
            <KPICard
              title="Trend 7 Tage"
              value="-0.15%"
              subtitle="Verbesserung"
              icon={TrendingDown}
              variant="success"
            />
            <KPICard
              title="Kosten"
              value={`€${totalCost.toLocaleString("de-DE", { minimumFractionDigits: 2 })}`}
              trend={2.1}
              trendLabel="vs. Vormonat"
              icon={Euro}
              variant="danger"
            />
          </div>

          {/* Charts Row */}
          <div className="mb-6 grid gap-6 lg:grid-cols-2">
            <ChartCard title="Konzessionsrate Trend" subtitle="Letzte 30 Tage">
              <div className="h-64">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={dailyMetrics}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#333" />
                    <XAxis
                      dataKey="date"
                      stroke="#666"
                      fontSize={10}
                      tickFormatter={(date) =>
                        new Date(date).toLocaleDateString("de-DE", { day: "2-digit", month: "2-digit" })
                      }
                    />
                    <YAxis stroke="#666" fontSize={10} tickFormatter={(v) => `${v}%`} />
                    <Tooltip
                      contentStyle={{ backgroundColor: "#1a1a2e", border: "1px solid #333", borderRadius: "8px" }}
                      labelStyle={{ color: "#999" }}
                      formatter={(value: number) => [`${value.toFixed(2)}%`, "Rate"]}
                      labelFormatter={(date) => new Date(date).toLocaleDateString("de-DE")}
                    />
                    <Line
                      type="monotone"
                      dataKey="rate"
                      stroke="#6366f1"
                      strokeWidth={2}
                      dot={false}
                      activeDot={{ r: 4, fill: "#6366f1" }}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </ChartCard>

            <ChartCard title="Konzessionsarten" subtitle="Verteilung nach Typ">
              <div className="h-64 flex items-center">
                <ResponsiveContainer width="50%" height="100%">
                  <PieChart>
                    <Pie
                      data={concessionTypes}
                      cx="50%"
                      cy="50%"
                      innerRadius={50}
                      outerRadius={80}
                      paddingAngle={2}
                      dataKey="count"
                    >
                      {concessionTypes.map((_, index) => (
                        <Cell key={`cell-${index}`} fill={CHART_COLORS[index % CHART_COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip
                      contentStyle={{ backgroundColor: "#1a1a2e", border: "1px solid #333", borderRadius: "8px" }}
                      formatter={(value: number, name: string, props) => [value, props.payload.type]}
                    />
                  </PieChart>
                </ResponsiveContainer>
                <div className="flex-1 space-y-2">
                  {concessionTypes.map((type, index) => (
                    <div key={type.type} className="flex items-center gap-2">
                      <div className="h-3 w-3 rounded-full" style={{ backgroundColor: CHART_COLORS[index] }} />
                      <span className="text-sm text-muted-foreground">{type.type}</span>
                      <span className="ml-auto text-sm font-medium text-foreground">{type.percentage}%</span>
                    </div>
                  ))}
                </div>
              </div>
            </ChartCard>
          </div>

          {/* Driver Tables */}
          <div className="grid gap-6 lg:grid-cols-2">
            <ChartCard title="Hochrisiko-Fahrer" subtitle="Coaching erforderlich">
              <DataTable
                data={highRiskDrivers}
                columns={driverColumns}
                onRowClick={(driver) => console.log("Navigate to driver:", driver.id)}
              />
            </ChartCard>

            <ChartCard title="Top-Performer" subtitle="Beste Fahrer">
              <DataTable
                data={topPerformers}
                columns={driverColumns}
                onRowClick={(driver) => console.log("Navigate to driver:", driver.id)}
              />
            </ChartCard>
          </div>

          <div className="mt-6">
            <PatternsPanel />
          </div>
        </div>
      </main>
    </div>
  )
}

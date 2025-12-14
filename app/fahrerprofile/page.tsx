"use client"

import { useMemo, useState } from "react"
import { Sidebar } from "@/components/dashboard/sidebar"
import { Header } from "@/components/dashboard/header"
import { KPICard } from "@/components/dashboard/kpi-card"
import { ChartCard } from "@/components/dashboard/chart-card"
import { DataTable } from "@/components/dashboard/data-table"
import { StatusBadge } from "@/components/dashboard/status-badge"
import { generateDrivers, depots, generateDailyMetrics } from "@/lib/mock-data"
import { Users, Search, Filter, FileText, ArrowLeft, MapPin, Phone, Calendar, TrendingUp, Target } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from "recharts"

export default function DriverProfilesPage() {
  const [selectedDriver, setSelectedDriver] = useState<(typeof drivers)[0] | null>(null)
  const [searchQuery, setSearchQuery] = useState("")
  const [depotFilter, setDepotFilter] = useState<string>("all")

  const drivers = useMemo(() => generateDrivers(100), [])
  const driverMetrics = useMemo(() => generateDailyMetrics(14), [])

  const filteredDrivers = useMemo(() => {
    return drivers.filter((driver) => {
      const matchesSearch =
        driver.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        driver.id.toLowerCase().includes(searchQuery.toLowerCase())
      const matchesDepot = depotFilter === "all" || driver.depotId === depotFilter
      return matchesSearch && matchesDepot
    })
  }, [drivers, searchQuery, depotFilter])

  const getRiskStatus = (score: number): "success" | "warning" | "danger" => {
    if (score >= 70) return "danger"
    if (score >= 40) return "warning"
    return "success"
  }

  const driverColumns = [
    { key: "name", header: "Name" },
    { key: "id", header: "ID", className: "text-muted-foreground font-mono text-xs" },
    { key: "depotId", header: "Depot" },
    {
      key: "deliveries",
      header: "Lieferungen",
      render: (d: (typeof drivers)[0]) => d.deliveries.toLocaleString("de-DE"),
    },
    {
      key: "concessionRate",
      header: "Rate",
      render: (d: (typeof drivers)[0]) => `${d.concessionRate.toFixed(2)}%`,
    },
    {
      key: "riskScore",
      header: "Risiko",
      render: (d: (typeof drivers)[0]) => (
        <StatusBadge
          status={getRiskStatus(d.riskScore)}
          label={d.riskScore >= 70 ? "Hoch" : d.riskScore >= 40 ? "Mittel" : "Niedrig"}
        />
      ),
    },
  ]

  // Generate coaching factors for selected driver
  const coachingFactors = selectedDriver
    ? [
        { factor: "Kontaktrate", value: selectedDriver.contactRate, target: 85, unit: "%" },
        { factor: "Geo-Abweichung", value: selectedDriver.geoMismatchRate, target: 2, unit: "%" },
        { factor: "Konzessionsrate", value: selectedDriver.concessionRate, target: 5, unit: "%" },
        { factor: "Trend 7d", value: selectedDriver.trend, target: 0, unit: "%" },
      ]
    : []

  if (selectedDriver) {
    return (
      <div className="flex min-h-screen">
        <Sidebar />
        <main className="ml-64 flex-1">
          <Header title="Fahrerprofil" subtitle={selectedDriver.name} />

          <div className="p-6">
            {/* Back Button */}
            <Button variant="ghost" size="sm" className="mb-6 gap-2" onClick={() => setSelectedDriver(null)}>
              <ArrowLeft className="h-4 w-4" />
              Zurück zur Übersicht
            </Button>

            {/* Driver Header */}
            <div className="mb-6 rounded-lg border border-border bg-card p-6">
              <div className="flex items-start justify-between">
                <div className="flex items-center gap-4">
                  <div className="flex h-16 w-16 items-center justify-center rounded-full bg-primary text-2xl font-bold text-primary-foreground">
                    {selectedDriver.name
                      .split(" ")
                      .map((n) => n[0])
                      .join("")}
                  </div>
                  <div>
                    <h2 className="text-xl font-semibold text-foreground">{selectedDriver.name}</h2>
                    <p className="text-sm text-muted-foreground font-mono">{selectedDriver.id}</p>
                    <div className="mt-2 flex items-center gap-4 text-sm text-muted-foreground">
                      <span className="flex items-center gap-1">
                        <MapPin className="h-4 w-4" />
                        {depots.find((d) => d.id === selectedDriver.depotId)?.name || selectedDriver.depotId}
                      </span>
                      <span className="flex items-center gap-1">
                        <Calendar className="h-4 w-4" />
                        Seit März 2023
                      </span>
                    </div>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <StatusBadge
                    status={getRiskStatus(selectedDriver.riskScore)}
                    label={`Risiko: ${selectedDriver.riskScore}`}
                    size="md"
                  />
                  <Button variant="outline" className="gap-2 bg-transparent">
                    <FileText className="h-4 w-4" />
                    Coaching-Protokoll
                  </Button>
                </div>
              </div>
            </div>

            {/* KPI Row */}
            <div className="mb-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
              <KPICard
                title="Lieferungen"
                value={selectedDriver.deliveries.toLocaleString("de-DE")}
                subtitle="Letzte 30 Tage"
              />
              <KPICard
                title="Konzessionsrate"
                value={`${selectedDriver.concessionRate.toFixed(2)}%`}
                trend={selectedDriver.trend}
                trendLabel="vs. Vorwoche"
                variant={
                  selectedDriver.concessionRate > 7
                    ? "danger"
                    : selectedDriver.concessionRate > 5
                      ? "warning"
                      : "success"
                }
              />
              <KPICard
                title="Kontaktrate"
                value={`${selectedDriver.contactRate}%`}
                subtitle={selectedDriver.contactRate >= 80 ? "Im Zielbereich" : "Unter Ziel"}
                variant={selectedDriver.contactRate >= 80 ? "success" : "warning"}
              />
              <KPICard
                title="Gesamtkosten"
                value={`€${selectedDriver.costTotal.toLocaleString("de-DE", { minimumFractionDigits: 2 })}`}
                subtitle="Konzessionskosten"
                variant="danger"
              />
            </div>

            {/* Charts */}
            <div className="mb-6 grid gap-6 lg:grid-cols-2">
              <ChartCard title="Konzessionsrate Verlauf" subtitle="Letzte 14 Tage">
                <div className="h-64">
                  <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={driverMetrics}>
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
                        formatter={(value: number) => [`${value.toFixed(2)}%`, "Rate"]}
                        labelFormatter={(date) => new Date(date).toLocaleDateString("de-DE")}
                      />
                      {/* Target line */}
                      <Line type="monotone" dataKey={() => 5} stroke="#22c55e" strokeDasharray="5 5" dot={false} />
                      <Line
                        type="monotone"
                        dataKey="rate"
                        stroke="#6366f1"
                        strokeWidth={2}
                        dot={false}
                        activeDot={{ r: 4 }}
                      />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
                <div className="mt-2 flex items-center justify-center gap-4 text-xs">
                  <div className="flex items-center gap-2">
                    <div className="h-0.5 w-4 bg-primary" />
                    <span className="text-muted-foreground">Aktuelle Rate</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <div className="h-0.5 w-4 bg-success" style={{ borderStyle: "dashed" }} />
                    <span className="text-muted-foreground">Zielwert (5%)</span>
                  </div>
                </div>
              </ChartCard>

              <ChartCard title="Coaching-Faktoren" subtitle="Vergleich mit Zielwerten">
                <div className="h-64">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={coachingFactors} layout="vertical">
                      <CartesianGrid strokeDasharray="3 3" stroke="#333" horizontal={false} />
                      <XAxis type="number" stroke="#666" fontSize={10} />
                      <YAxis type="category" dataKey="factor" stroke="#666" fontSize={10} width={100} />
                      <Tooltip
                        contentStyle={{ backgroundColor: "#1a1a2e", border: "1px solid #333", borderRadius: "8px" }}
                        formatter={(value: number, name: string) => [`${value}`, name === "value" ? "Aktuell" : "Ziel"]}
                      />
                      <Bar dataKey="value" fill="#6366f1" radius={[0, 4, 4, 0]} name="Aktuell" />
                      <Bar dataKey="target" fill="#22c55e" radius={[0, 4, 4, 0]} name="Ziel" />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </ChartCard>
            </div>

            {/* Coaching Recommendations */}
            <ChartCard title="Coaching-Empfehlungen" subtitle="Basierend auf ML-Analyse">
              <div className="grid gap-4 sm:grid-cols-2">
                {[
                  {
                    title: "Kontaktrate verbessern",
                    description:
                      "Die Kontaktrate liegt unter dem Zielwert. Empfehlung: Mehr Zeit für Kundenkontakt einplanen.",
                    priority: "high",
                    icon: Phone,
                  },
                  {
                    title: "Morgenstunden-Muster",
                    description:
                      "Erhöhte Konzessionsrate zwischen 6-9 Uhr. Empfehlung: Zeitmanagement in Stoßzeiten überprüfen.",
                    priority: "medium",
                    icon: Calendar,
                  },
                  {
                    title: "Geo-Abweichung reduzieren",
                    description:
                      "GPS-Abweichungen über Durchschnitt. Empfehlung: Adressvalidierung vor Zustellung prüfen.",
                    priority: "medium",
                    icon: MapPin,
                  },
                  {
                    title: "Trend-Monitoring",
                    description: "Positive Entwicklung in den letzten 7 Tagen. Weiter beobachten und unterstützen.",
                    priority: "low",
                    icon: TrendingUp,
                  },
                ].map((rec, idx) => (
                  <div key={idx} className="rounded-lg border border-border bg-secondary/30 p-4">
                    <div className="flex items-start gap-3">
                      <div
                        className={`rounded-lg p-2 ${
                          rec.priority === "high"
                            ? "bg-destructive/10"
                            : rec.priority === "medium"
                              ? "bg-warning/10"
                              : "bg-success/10"
                        }`}
                      >
                        <rec.icon
                          className={`h-4 w-4 ${
                            rec.priority === "high"
                              ? "text-destructive"
                              : rec.priority === "medium"
                                ? "text-warning"
                                : "text-success"
                          }`}
                        />
                      </div>
                      <div>
                        <h4 className="font-medium text-foreground">{rec.title}</h4>
                        <p className="mt-1 text-sm text-muted-foreground">{rec.description}</p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </ChartCard>
          </div>
        </main>
      </div>
    )
  }

  return (
    <div className="flex min-h-screen">
      <Sidebar />
      <main className="ml-64 flex-1">
        <Header title="Fahrerprofile" subtitle="Individuelle Fahreranalyse und Coaching" />

        <div className="p-6">
          {/* KPI Row */}
          <div className="mb-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            <KPICard title="Gesamtfahrer" value={drivers.length} subtitle="Aktive Fahrer" icon={Users} />
            <KPICard
              title="Durchschnittliche Rate"
              value={`${(drivers.reduce((sum, d) => sum + d.concessionRate, 0) / drivers.length).toFixed(2)}%`}
              subtitle="Alle Fahrer"
              icon={Target}
            />
            <KPICard
              title="Coaching erforderlich"
              value={drivers.filter((d) => d.riskScore >= 70).length}
              subtitle="Hochrisiko-Fahrer"
              variant="danger"
            />
            <KPICard
              title="Top-Performer"
              value={drivers.filter((d) => d.riskScore < 30).length}
              subtitle="Niedriges Risiko"
              variant="success"
            />
          </div>

          {/* Filters */}
          <div className="mb-6 flex items-center gap-4">
            <div className="relative flex-1 max-w-md">
              <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
              <Input
                placeholder="Fahrer suchen (Name oder ID)..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-10 bg-secondary border-border"
              />
            </div>
            <Select value={depotFilter} onValueChange={setDepotFilter}>
              <SelectTrigger className="w-[200px] border-border bg-secondary">
                <Filter className="h-4 w-4 mr-2" />
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

          {/* Driver Table */}
          <ChartCard title="Fahrerliste" subtitle={`${filteredDrivers.length} Fahrer gefunden`}>
            <DataTable
              data={filteredDrivers.slice(0, 20)}
              columns={driverColumns}
              onRowClick={(driver) => setSelectedDriver(driver)}
            />
            {filteredDrivers.length > 20 && (
              <div className="mt-4 text-center text-sm text-muted-foreground">
                Zeige 20 von {filteredDrivers.length} Fahrern. Verwende die Suche zum Filtern.
              </div>
            )}
          </ChartCard>
        </div>
      </main>
    </div>
  )
}

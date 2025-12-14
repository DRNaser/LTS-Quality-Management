"use client"

import type React from "react"

import { useState } from "react"
import { Sidebar } from "@/components/dashboard/sidebar"
import { Header } from "@/components/dashboard/header"
import { KPICard } from "@/components/dashboard/kpi-card"
import { ChartCard } from "@/components/dashboard/chart-card"
import { StatusBadge } from "@/components/dashboard/status-badge"
import { depots } from "@/lib/mock-data"
import {
  Upload,
  FileSpreadsheet,
  Database,
  CheckCircle2,
  XCircle,
  Clock,
  Trash2,
  Download,
  Plus,
  Building2,
} from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"

interface UploadHistory {
  id: string
  filename: string
  depot: string
  date: string
  rows: number
  status: "success" | "error" | "processing"
  error?: string
}

const uploadHistory: UploadHistory[] = [
  { id: "1", filename: "KW50_DUS1_2024.xlsx", depot: "DUS1", date: "2024-12-13", rows: 12453, status: "success" },
  { id: "2", filename: "KW50_DUS2_2024.xlsx", depot: "DUS2", date: "2024-12-13", rows: 8234, status: "success" },
  { id: "3", filename: "KW50_CGN1_2024.xlsx", depot: "CGN1", date: "2024-12-13", rows: 15678, status: "success" },
  {
    id: "4",
    filename: "KW49_BER1_2024.xlsx",
    depot: "BER1",
    date: "2024-12-06",
    rows: 0,
    status: "error",
    error: "Ungültiges Spaltenformat",
  },
  { id: "5", filename: "KW49_MUC1_2024.xlsx", depot: "MUC1", date: "2024-12-06", rows: 9876, status: "success" },
]

export default function DataManagementPage() {
  const [selectedDepot, setSelectedDepot] = useState<string>("")
  const [isDragging, setIsDragging] = useState(false)
  const [uploadedFile, setUploadedFile] = useState<File | null>(null)
  const [isUploading, setIsUploading] = useState(false)

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(true)
  }

  const handleDragLeave = () => {
    setIsDragging(false)
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)
    const file = e.dataTransfer.files[0]
    if (file && (file.name.endsWith(".xlsx") || file.name.endsWith(".csv"))) {
      setUploadedFile(file)
    }
  }

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      setUploadedFile(file)
    }
  }

  const handleUpload = async () => {
    if (!uploadedFile || !selectedDepot) return
    setIsUploading(true)
    // Simulate upload
    await new Promise((resolve) => setTimeout(resolve, 2000))
    setIsUploading(false)
    setUploadedFile(null)
    setSelectedDepot("")
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case "success":
        return <CheckCircle2 className="h-4 w-4 text-success" />
      case "error":
        return <XCircle className="h-4 w-4 text-destructive" />
      case "processing":
        return <Clock className="h-4 w-4 text-warning animate-spin" />
      default:
        return null
    }
  }

  const totalRows = uploadHistory.filter((u) => u.status === "success").reduce((sum, u) => sum + u.rows, 0)
  const successCount = uploadHistory.filter((u) => u.status === "success").length
  const errorCount = uploadHistory.filter((u) => u.status === "error").length

  return (
    <div className="flex min-h-screen">
      <Sidebar />
      <main className="ml-64 flex-1">
        <Header title="Datenverwaltung" subtitle="Datenimport und Depotverwaltung" />

        <div className="p-6">
          {/* KPI Row */}
          <div className="mb-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            <KPICard title="Aktive Depots" value={depots.length} subtitle="Konfigurierte Standorte" icon={Building2} />
            <KPICard
              title="Datensätze"
              value={totalRows.toLocaleString("de-DE")}
              subtitle="Gesamte Lieferungen"
              icon={Database}
            />
            <KPICard
              title="Erfolgreiche Uploads"
              value={successCount}
              subtitle="Diese Woche"
              icon={CheckCircle2}
              variant="success"
            />
            <KPICard
              title="Fehlgeschlagen"
              value={errorCount}
              subtitle="Erfordern Korrektur"
              icon={XCircle}
              variant={errorCount > 0 ? "danger" : "success"}
            />
          </div>

          {/* Upload Section */}
          <div className="mb-6 grid gap-6 lg:grid-cols-2">
            {/* Upload Form */}
            <ChartCard title="Wöchentlicher Datenimport" subtitle="Excel- oder CSV-Datei hochladen">
              <div className="space-y-4">
                {/* Depot Selection */}
                <div className="space-y-2">
                  <Label>Depot auswählen</Label>
                  <Select value={selectedDepot} onValueChange={setSelectedDepot}>
                    <SelectTrigger className="border-border bg-secondary">
                      <SelectValue placeholder="Depot wählen..." />
                    </SelectTrigger>
                    <SelectContent>
                      {depots.map((depot) => (
                        <SelectItem key={depot.id} value={depot.id}>
                          {depot.name} ({depot.id})
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                {/* Drop Zone */}
                <div
                  className={`relative rounded-lg border-2 border-dashed p-8 text-center transition-colors ${
                    isDragging
                      ? "border-primary bg-primary/5"
                      : uploadedFile
                        ? "border-success bg-success/5"
                        : "border-border hover:border-primary/50"
                  }`}
                  onDragOver={handleDragOver}
                  onDragLeave={handleDragLeave}
                  onDrop={handleDrop}
                >
                  <input
                    type="file"
                    accept=".xlsx,.csv"
                    className="absolute inset-0 cursor-pointer opacity-0"
                    onChange={handleFileSelect}
                  />

                  {uploadedFile ? (
                    <div className="flex flex-col items-center gap-2">
                      <FileSpreadsheet className="h-10 w-10 text-success" />
                      <p className="font-medium text-foreground">{uploadedFile.name}</p>
                      <p className="text-sm text-muted-foreground">{(uploadedFile.size / 1024 / 1024).toFixed(2)} MB</p>
                      <Button variant="ghost" size="sm" onClick={() => setUploadedFile(null)}>
                        Datei entfernen
                      </Button>
                    </div>
                  ) : (
                    <div className="flex flex-col items-center gap-2">
                      <Upload className="h-10 w-10 text-muted-foreground" />
                      <p className="font-medium text-foreground">Datei hierher ziehen</p>
                      <p className="text-sm text-muted-foreground">oder klicken zum Auswählen</p>
                      <p className="text-xs text-muted-foreground">Unterstützt: .xlsx, .csv</p>
                    </div>
                  )}
                </div>

                {/* Upload Button */}
                <Button
                  className="w-full"
                  disabled={!uploadedFile || !selectedDepot || isUploading}
                  onClick={handleUpload}
                >
                  {isUploading ? (
                    <>
                      <Clock className="h-4 w-4 mr-2 animate-spin" />
                      Wird hochgeladen...
                    </>
                  ) : (
                    <>
                      <Upload className="h-4 w-4 mr-2" />
                      Daten importieren
                    </>
                  )}
                </Button>
              </div>
            </ChartCard>

            {/* Expected Format */}
            <ChartCard title="Erwartetes Datenformat" subtitle="Erforderliche Spalten">
              <div className="space-y-3">
                {[
                  { name: "transporter_id", type: "String", desc: "Fahrer-ID" },
                  { name: "tracking_id", type: "String", desc: "Paketnummer" },
                  { name: "delivery_date_time", type: "DateTime", desc: "Zeitstempel" },
                  { name: "station / dsp", type: "String", desc: "Depot-ID" },
                  { name: "zip_code", type: "String", desc: "Postleitzahl" },
                  { name: "Delivered to Neighbour", type: "Binary", desc: "Konzessions-Flag" },
                  { name: "contact", type: "Boolean", desc: "Kundenkontakt" },
                  { name: "Geo Distance > 25m", type: "Binary", desc: "GPS-Abweichung" },
                  { name: "Concession Cost", type: "Float", desc: "Kosten in EUR" },
                ].map((col, idx) => (
                  <div
                    key={idx}
                    className="flex items-center justify-between rounded-lg bg-secondary/50 px-3 py-2 text-sm"
                  >
                    <div>
                      <span className="font-mono text-primary">{col.name}</span>
                      <span className="ml-2 text-muted-foreground">- {col.desc}</span>
                    </div>
                    <span className="text-xs text-muted-foreground">{col.type}</span>
                  </div>
                ))}
              </div>
            </ChartCard>
          </div>

          {/* Upload History */}
          <ChartCard
            title="Upload-Historie"
            subtitle="Letzte Datenimporte"
            action={
              <Button variant="outline" size="sm" className="gap-2 bg-transparent">
                <Download className="h-4 w-4" />
                Export Log
              </Button>
            }
          >
            <div className="space-y-2">
              {uploadHistory.map((upload) => (
                <div
                  key={upload.id}
                  className="flex items-center justify-between rounded-lg border border-border bg-secondary/30 px-4 py-3"
                >
                  <div className="flex items-center gap-4">
                    {getStatusIcon(upload.status)}
                    <div>
                      <p className="font-medium text-foreground">{upload.filename}</p>
                      <p className="text-sm text-muted-foreground">
                        {upload.depot} • {new Date(upload.date).toLocaleDateString("de-DE")}
                      </p>
                      {upload.error && <p className="text-sm text-destructive">{upload.error}</p>}
                    </div>
                  </div>
                  <div className="flex items-center gap-4">
                    {upload.status === "success" && (
                      <span className="text-sm text-muted-foreground">
                        {upload.rows.toLocaleString("de-DE")} Zeilen
                      </span>
                    )}
                    <StatusBadge
                      status={
                        upload.status === "success" ? "success" : upload.status === "error" ? "danger" : "warning"
                      }
                      label={
                        upload.status === "success"
                          ? "Erfolgreich"
                          : upload.status === "error"
                            ? "Fehler"
                            : "Verarbeitung"
                      }
                    />
                  </div>
                </div>
              ))}
            </div>
          </ChartCard>

          {/* Depot Management */}
          <div className="mt-6">
            <ChartCard
              title="Depotverwaltung"
              subtitle="Konfigurierte Standorte"
              action={
                <Dialog>
                  <DialogTrigger asChild>
                    <Button size="sm" className="gap-2">
                      <Plus className="h-4 w-4" />
                      Neues Depot
                    </Button>
                  </DialogTrigger>
                  <DialogContent>
                    <DialogHeader>
                      <DialogTitle>Neues Depot hinzufügen</DialogTitle>
                      <DialogDescription>Fügen Sie ein neues Depot zur Verwaltung hinzu.</DialogDescription>
                    </DialogHeader>
                    <div className="space-y-4 py-4">
                      <div className="space-y-2">
                        <Label>Depot-ID</Label>
                        <Input placeholder="z.B. HAM1" />
                      </div>
                      <div className="space-y-2">
                        <Label>Name</Label>
                        <Input placeholder="z.B. Hamburg Zentrum" />
                      </div>
                      <div className="space-y-2">
                        <Label>Region</Label>
                        <Input placeholder="z.B. Hamburg" />
                      </div>
                    </div>
                    <DialogFooter>
                      <Button variant="outline">Abbrechen</Button>
                      <Button>Depot erstellen</Button>
                    </DialogFooter>
                  </DialogContent>
                </Dialog>
              }
            >
              <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
                {depots.map((depot) => (
                  <div key={depot.id} className="rounded-lg border border-border bg-secondary/30 p-4">
                    <div className="flex items-start justify-between">
                      <div>
                        <div className="flex items-center gap-2">
                          <Building2 className="h-4 w-4 text-primary" />
                          <span className="font-medium text-foreground">{depot.id}</span>
                        </div>
                        <p className="mt-1 text-sm text-foreground">{depot.name}</p>
                        <p className="text-xs text-muted-foreground">{depot.region}</p>
                      </div>
                      <Button variant="ghost" size="icon" className="text-muted-foreground hover:text-destructive">
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    </div>
                    <div className="mt-3 flex items-center gap-2">
                      <div className="h-2 w-2 rounded-full bg-success" />
                      <span className="text-xs text-muted-foreground">Aktiv</span>
                    </div>
                  </div>
                ))}
              </div>
            </ChartCard>
          </div>
        </div>
      </main>
    </div>
  )
}

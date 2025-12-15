import { render, screen, waitFor } from "@testing-library/react"
import userEvent from "@testing-library/user-event"
import { PatternsPanel } from "@/components/dashboard/patterns-panel"
import { ConcessionEvent } from "@/lib/pattern-analyzer"

type MockResponse = {
  ok?: boolean
  patterns: any[]
  trends: any[]
  json?: () => Promise<any>
}

describe("PatternsPanel", () => {
  const basePatterns = [
    {
      id: "driver-123",
      type: "driver_hotspot",
      description: "Fahrer 123 zeigt erhöhte Konzessionsrate (18.0%)",
      severity: "high",
      confidence: 0.82,
      drivers: ["DRV-001"],
      depotId: "DUS1",
    },
  ]

  const baseTrends = [
    {
      driverId: "DRV-001",
      direction: "increasing",
      change: 4.5,
      significance: 0.9,
    },
  ]

  const mockEvents: ConcessionEvent[] = [
    {
      id: "1",
      driverId: "DRV-001",
      depotId: "DUS1",
      timestamp: new Date().toISOString(),
      isConcession: true,
      type: "Nachbar",
    },
  ]

  const createFetcher = (responses: MockResponse[]) =>
    jest.fn().mockImplementation(() => {
      const next = responses.shift()
      if (!next) throw new Error("No response configured")
      return Promise.resolve({
        ok: next.ok ?? true,
        json: next.json ?? (() => Promise.resolve({ patterns: next.patterns, trends: next.trends })),
      })
    })

  it("renders detected patterns with severity and confidence", async () => {
    const fetcher = createFetcher([{ patterns: basePatterns, trends: baseTrends }])

    render(<PatternsPanel fetcher={fetcher} seedEvents={mockEvents} />)

    await waitFor(() => {
      expect(screen.getByTestId("pattern-results")).toHaveTextContent("driver_hotspot")
    })

    expect(screen.getByText("HIGH")).toBeInTheDocument()
    expect(screen.getByText(/Vertrauen/)).toHaveTextContent("82%")
    expect(screen.getByText(/Fahrer DRV-001/)).toBeInTheDocument()
    expect(screen.getByTestId("trend-summary")).toHaveTextContent("Steigend")
  })

  it("supports filtering by depot and driver", async () => {
    const fetcher = createFetcher([
      { patterns: basePatterns, trends: baseTrends },
      {
        patterns: [
          {
            ...basePatterns[0],
            depotId: "BER1",
            drivers: ["DRV-002"],
            id: "driver-002",
          },
        ],
        trends: baseTrends,
      },
    ])

    render(<PatternsPanel fetcher={fetcher} seedEvents={mockEvents} />)

    await waitFor(() => expect(fetcher).toHaveBeenCalledTimes(1))

    await userEvent.selectOptions(screen.getByTestId("depot-filter"), "BER1")
    await waitFor(() => expect(fetcher).toHaveBeenCalledTimes(2))
    expect(screen.getByText(/Depot BER1/)).toBeInTheDocument()
  })

  it("shows empty state when no patterns are returned", async () => {
    const fetcher = createFetcher([{ patterns: [], trends: [] }])

    render(<PatternsPanel fetcher={fetcher} seedEvents={mockEvents} />)

    expect(await screen.findByTestId("empty-state")).toBeInTheDocument()
  })

  it("shows error state on failure", async () => {
    const fetcher = jest.fn().mockRejectedValue(new Error("Analyzer offline"))

    render(<PatternsPanel fetcher={fetcher} seedEvents={mockEvents} />)

    expect(await screen.findByTestId("error-state")).toHaveTextContent("Analyzer offline")
  })
})

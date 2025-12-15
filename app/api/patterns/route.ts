import { NextResponse } from "next/server"
import { AnalyzerFilters, PatternAnalyzer } from "@/lib/pattern-analyzer"

export async function POST(request: Request) {
  try {
    const body = await request.json()
    const events = Array.isArray(body?.events) ? body.events : []
    const filters: AnalyzerFilters = body?.filters || {}

    if (!events.length) {
      return NextResponse.json(
        { message: "No concession events provided", patterns: [], trends: [] },
        { status: 400 }
      )
    }

    const analyzer = new PatternAnalyzer()
    const { patterns, trends } = analyzer.analyze(events, filters)

    return NextResponse.json({ patterns, trends })
  } catch (error) {
    console.error("Pattern analysis failed", error)
    return NextResponse.json(
      { message: "Failed to analyze patterns" },
      { status: 500 }
    )
  }
}

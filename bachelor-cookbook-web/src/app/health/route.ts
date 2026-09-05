import { NextResponse } from "next/server";

/** Public liveness — no secrets, no Flux, no auth state. */
export async function GET() {
  return NextResponse.json({ ok: true, service: "bachelor-cookbook" });
}

import { render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import App from "./App";

vi.mock("./lib/api", () => ({
  getHealth: vi.fn().mockRejectedValue(new Error("offline")),
}));

describe("TxnVeyra shell", () => {
  it("renders the product name and prototype status", () => {
    render(<App />);
    expect(screen.getByText("TxnVeyra")).toBeInTheDocument();
    expect(screen.getByText("Development environment")).toBeInTheDocument();
    expect(screen.getByText("PROTOTYPE")).toBeInTheDocument();
  });
});

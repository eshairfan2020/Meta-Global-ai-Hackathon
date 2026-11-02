export type Lang = "en" | "ur";
export type RiskBand = "high_concern" | "some_concern" | "insufficient_evidence";
export type VStatus =
  | "not_checked" | "attempting_independent_contact" | "user_recorded_confirmation"
  | "user_recorded_denial" | "inconclusive";

export interface Example { id: string; title_en: string; title_ur: string; text: string }
export interface WarningSignal { label: string; source_quote: string; explanation: string }
export interface Assessment {
  risk_band: RiskBand;
  scam_category: string;
  observed_facts: {
    claimed_identity: string | null; requested_action: string | null; amount: string | null;
    urgency_present: boolean; secrecy_present: boolean; verification_code_requested: boolean;
  };
  warning_signals: WarningSignal[];
  uncertainty: string;
  recommended_actions: string[];
  safe_reply: string;
  family_verification_suggested: boolean;
}
export interface CaseView {
  case_id: string; created_at: string; language: Lang; is_synthetic: boolean; example_id: string | null;
  provider: "ollama" | "mock"; model: string | null; inference: "real" | "simulated";
  latency_ms: number | null; redactions: number; quotes_removed: number; amount_cleared: boolean;
  rules_triggered?: string[]; rule_adjusted?: boolean;
  assessment: Assessment;
  verification: { status: VStatus; events: { status: VStatus; timestamp: string }[] };
}
export interface ModelStatus {
  provider: "ollama" | "mock"; model: string | null;
  state: "ready" | "unreachable" | "model_not_installed" | "mock"; detail: string;
}

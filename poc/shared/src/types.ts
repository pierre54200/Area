export type WorkflowStatus = "draft" | "enabled" | "disabled";
export interface WorkflowSummary { id: string; name: string; enabled: boolean; }
export interface ApiError { code: string; message: string; }

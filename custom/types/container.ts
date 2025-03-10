export interface ContainerStatus {
    status: string;
    health: string;
    current_version: string;
    latest_version: string;
    update_available: boolean;
    created: string;
}

export interface ContainerResponse {
    success: boolean;
    data?: ContainerStatus;
    message?: string;
} 
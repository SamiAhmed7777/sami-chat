export async function executeAction<T>(actionId: string, params?: Record<string, unknown>): Promise<T> {
    // This is a mock implementation for testing
    const mockResponses = {
        container_status: {
            success: true,
            data: {
                status: "running",
                health: "healthy",
                current_version: "1.0.0",
                latest_version: "1.1.0",
                update_available: true,
                created: new Date().toISOString()
            }
        },
        update_container: {
            success: true,
            message: "Update initiated"
        }
    };

    return new Promise((resolve) => {
        setTimeout(() => {
            resolve(mockResponses[actionId as keyof typeof mockResponses] as T);
        }, 500);
    });
} 
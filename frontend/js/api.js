// API endpoints
const API_URL = "http://localhost:3000";

// API object
const API = {
    auth: {
        login: async (username, password) => {
            try {
                const response = await fetch(`${API_URL}/api/auth/login`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ username, password }),
                });
                return await response.json();
            } catch (error) {
                console.error("Login error:", error);
                return { success: false, message: "Lỗi kết nối đến máy chủ" };
            }
        },
        verify: async () => {
            try {
                const token = localStorage.getItem("token");
                if (!token) return { success: false };

                const response = await fetch(`${API_URL}/api/auth/verify`, {
                    method: "GET",
                    headers: {
                        "x-auth-token": token,
                    },
                });
                return await response.json();
            } catch (error) {
                console.error("Verify error:", error);
                return { success: false };
            }
        },
        getProfile: async () => {
            try {
                const token = localStorage.getItem("token");
                if (!token) return { success: false };

                const response = await fetch(`${API_URL}/api/auth/me`, {
                    method: "GET",
                    headers: {
                        "x-auth-token": token,
                    },
                });
                return await response.json();
            } catch (error) {
                console.error("Get profile error:", error);
                return { success: false };
            }
        }
    },
    vehicle: {
        getAllVehicles: async () => {
            try {
                const token = localStorage.getItem("token");
                if (!token) return { success: false };

                const response = await fetch(`${API_URL}/api/vehicles`, {
                    method: "GET",
                    headers: {
                        "x-auth-token": token,
                    },
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                return await response.json();
            } catch (error) {
                console.error("Get all vehicles error:", error);
                throw error;
            }
        },
        getVehicleById: async (id) => {
            try {
                const token = localStorage.getItem("token");
                if (!token) return { success: false };

                const response = await fetch(`${API_URL}/api/vehicles/${id}`, {
                    method: "GET",
                    headers: {
                        "x-auth-token": token,
                    },
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                return await response.json();
            } catch (error) {
                console.error("Get vehicle by ID error:", error);
                throw error;
            }
        },
        getVehicleByLicensePlate: async (licensePlate) => {
            try {
                const token = localStorage.getItem("token");
                if (!token) return { success: false };

                const response = await fetch(`${API_URL}/api/vehicles/plate/${licensePlate}`, {
                    method: "GET",
                    headers: {
                        "x-auth-token": token,
                    },
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                return await response.json();
            } catch (error) {
                console.error("Get vehicle by license plate error:", error);
                throw error;
            }
        },
        createVehicle: async (vehicleData) => {
            try {
                const token = localStorage.getItem("token");
                if (!token) return { success: false };

                const response = await fetch(`${API_URL}/api/vehicles`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "x-auth-token": token,
                    },
                    body: JSON.stringify(vehicleData),
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                return await response.json();
            } catch (error) {
                console.error("Create vehicle error:", error);
                throw error;
            }
        },
        updateVehicle: async (id, vehicleData) => {
            try {
                const token = localStorage.getItem("token");
                if (!token) return { success: false };

                const response = await fetch(`${API_URL}/api/vehicles/${id}`, {
                    method: "PUT",
                    headers: {
                        "Content-Type": "application/json",
                        "x-auth-token": token,
                    },
                    body: JSON.stringify(vehicleData),
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                return await response.json();
            } catch (error) {
                console.error("Update vehicle error:", error);
                throw error;
            }
        },
        deleteVehicle: async (id) => {
            try {
                const token = localStorage.getItem("token");
                if (!token) return { success: false };

                const response = await fetch(`${API_URL}/api/vehicles/${id}`, {
                    method: "DELETE",
                    headers: {
                        "x-auth-token": token,
                    },
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                return await response.json();
            } catch (error) {
                console.error("Delete vehicle error:", error);
                throw error;
            }
        }
    },
    training: {
        startTraining: async (trainingData) => {
            try {
                const token = localStorage.getItem("token");
                if (!token) return { success: false };

                const response = await fetch(`${API_URL}/api/training/start`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "x-auth-token": token,
                    },
                    body: JSON.stringify(trainingData),
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                return await response.json();
            } catch (error) {
                console.error("Start training error:", error);
                throw error;
            }
        },
        getTrainingStatus: async (jobId) => {
            try {
                const token = localStorage.getItem("token");
                if (!token) return { success: false };

                const response = await fetch(`${API_URL}/api/training/jobs/${jobId}/status`, {
                    method: "GET",
                    headers: {
                        "x-auth-token": token,
                    },
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                return await response.json();
            } catch (error) {
                console.error("Get training status error:", error);
                throw error;
            }
        },
        saveModel: async (jobId, modelName, notes) => {
            try {
                const token = localStorage.getItem("token");
                if (!token) return { success: false, error: "Không tìm thấy token xác thực" };

                const response = await fetch(`${API_URL}/api/training/jobs/${jobId}/save-model`, {
                    method: "POST",
                    headers: {
                        "x-auth-token": token,
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ model_name: modelName, notes: notes }),
                });

                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(errorData.error || `Lỗi HTTP! status: ${response.status}`);
                }

                return await response.json();
            } catch (error) {
                console.error("Save model error:", error);
                return { success: false, error: error.message };
            }
        },
        discardModel: async (jobId) => {
            try {
                const token = localStorage.getItem("token");
                if (!token) return { success: false };

                const response = await fetch(`${API_URL}/api/training/jobs/${jobId}/discard-model`, {
                    method: "POST",
                    headers: {
                        "x-auth-token": token,
                    },
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                return await response.json();
            } catch (error) {
                console.error("Discard model error:", error);
                throw error;
            }
        }
    },
    prediction: {
        // ... các API liên quan đến prediction
    },
    // Thêm API cho thống kê mô hình
    stats: {
        getModelPerformanceStats: async () => {
            try {
                const token = localStorage.getItem("token");
                if (!token) return { success: false };

                const response = await fetch(`${API_URL}/api/stats/model-performance`, {
                    method: "GET",
                    headers: {
                        "x-auth-token": token,
                    },
                });
                return await response.json();
            } catch (error) {
                console.error("Get model stats error:", error);
                return { success: false, error: "Lỗi kết nối đến máy chủ" };
            }
        },
        getTrainingTrends: async () => {
            try {
                const token = localStorage.getItem("token");
                if (!token) return { success: false };

                const response = await fetch(`${API_URL}/api/stats/training-trends`, {
                    method: "GET",
                    headers: {
                        "x-auth-token": token,
                    },
                });
                return await response.json();
            } catch (error) {
                console.error("Get training trends error:", error);
                return { success: false, error: "Lỗi kết nối đến máy chủ" };
            }
        },
        getPredictionUsage: async () => {
            try {
                const token = localStorage.getItem("token");
                if (!token) return { success: false };

                const response = await fetch(`${API_URL}/api/stats/prediction-usage`, {
                    method: "GET",
                    headers: {
                        "x-auth-token": token,
                    },
                });
                return await response.json();
            } catch (error) {
                console.error("Get prediction usage error:", error);
                return { success: false, error: "Lỗi kết nối đến máy chủ" };
            }
        }
    },
    dataset: {
        getDatasets: async () => {
            try {
                const token = localStorage.getItem("token");
                if (!token) return { success: false, error: "Không tìm thấy token xác thực" };

                const response = await fetch(`http://localhost:3003/api/dataset`, {
                    method: "GET",
                    headers: {
                        "x-auth-token": token,
                    },
                });

                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(errorData.error || `Lỗi HTTP! status: ${response.status}`);
                }

                return await response.json();
            } catch (error) {
                console.error("Error fetching datasets:", error);
                return { success: false, error: error.message };
            }
        },
        uploadImages: async (formData) => {
            try {
                const token = localStorage.getItem("token");
                if (!token) return { success: false, error: "Không tìm thấy token xác thực" };

                const response = await fetch(`http://localhost:3003/api/dataset/upload-images`, {
                    method: "POST",
                    headers: {
                        "x-auth-token": token,
                        // Don't set Content-Type header for FormData, browser sets it automatically with correct boundary
                    },
                    body: formData,
                });

                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(errorData.error || `Lỗi HTTP! status: ${response.status}`);
                }

                return await response.json();
            } catch (error) {
                console.error("Error uploading images:", error);
                return { success: false, error: error.message };
            }
        },
        uploadZip: async (formData) => {
            try {
                const token = localStorage.getItem("token");
                if (!token) return { success: false, error: "Không tìm thấy token xác thực" };

                const response = await fetch(`http://localhost:3003/api/dataset/upload-zip`, {
                    method: "POST",
                    headers: {
                        "x-auth-token": token,
                    },
                    body: formData,
                });

                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(errorData.error || `Lỗi HTTP! status: ${response.status}`);
                }

                return await response.json();
            } catch (error) {
                console.error("Error uploading ZIP dataset:", error);
                return { success: false, error: error.message };
            }
        },
        getDatasetPreview: async (datasetId) => {
            try {
                const token = localStorage.getItem("token");
                if (!token) return { success: false, error: "Không tìm thấy token xác thực" };

                const response = await fetch(`http://localhost:3003/api/dataset/${datasetId}/preview`, {
                    method: "GET",
                    headers: {
                        "x-auth-token": token,
                    },
                });

                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(errorData.error || `Lỗi HTTP! status: ${response.status}`);
                }

                return await response.json();
            } catch (error) {
                console.error("Error getting dataset preview:", error);
                return { success: false, error: error.message };
            }
        },
        deleteDataset: async (datasetId) => {
            try {
                const token = localStorage.getItem("token");
                if (!token) return { success: false, error: "Không tìm thấy token xác thực" };

                const response = await fetch(`http://localhost:3003/api/dataset/${datasetId}`, {
                    method: "DELETE",
                    headers: {
                        "x-auth-token": token,
                    },
                });

                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(errorData.error || `Lỗi HTTP! status: ${response.status}`);
                }

                return await response.json();
            } catch (error) {
                console.error("Error deleting dataset:", error);
                return { success: false, error: error.message };
            }
        }
    }
};

// For use in browser
window.API = API;

// For use in browser
if (typeof module !== 'undefined' && module.exports) {
    module.exports = API;
}


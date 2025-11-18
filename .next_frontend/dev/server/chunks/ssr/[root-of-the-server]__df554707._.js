module.exports = [
"[externals]/next/dist/compiled/next-server/app-page-turbo.runtime.dev.js [external] (next/dist/compiled/next-server/app-page-turbo.runtime.dev.js, cjs)", ((__turbopack_context__, module, exports) => {

const mod = __turbopack_context__.x("next/dist/compiled/next-server/app-page-turbo.runtime.dev.js", () => require("next/dist/compiled/next-server/app-page-turbo.runtime.dev.js"));

module.exports = mod;
}),
"[externals]/next/dist/server/app-render/action-async-storage.external.js [external] (next/dist/server/app-render/action-async-storage.external.js, cjs)", ((__turbopack_context__, module, exports) => {

const mod = __turbopack_context__.x("next/dist/server/app-render/action-async-storage.external.js", () => require("next/dist/server/app-render/action-async-storage.external.js"));

module.exports = mod;
}),
"[externals]/next/dist/server/app-render/work-unit-async-storage.external.js [external] (next/dist/server/app-render/work-unit-async-storage.external.js, cjs)", ((__turbopack_context__, module, exports) => {

const mod = __turbopack_context__.x("next/dist/server/app-render/work-unit-async-storage.external.js", () => require("next/dist/server/app-render/work-unit-async-storage.external.js"));

module.exports = mod;
}),
"[externals]/next/dist/server/app-render/work-async-storage.external.js [external] (next/dist/server/app-render/work-async-storage.external.js, cjs)", ((__turbopack_context__, module, exports) => {

const mod = __turbopack_context__.x("next/dist/server/app-render/work-async-storage.external.js", () => require("next/dist/server/app-render/work-async-storage.external.js"));

module.exports = mod;
}),
"[externals]/util [external] (util, cjs)", ((__turbopack_context__, module, exports) => {

const mod = __turbopack_context__.x("util", () => require("util"));

module.exports = mod;
}),
"[externals]/stream [external] (stream, cjs)", ((__turbopack_context__, module, exports) => {

const mod = __turbopack_context__.x("stream", () => require("stream"));

module.exports = mod;
}),
"[externals]/path [external] (path, cjs)", ((__turbopack_context__, module, exports) => {

const mod = __turbopack_context__.x("path", () => require("path"));

module.exports = mod;
}),
"[externals]/http [external] (http, cjs)", ((__turbopack_context__, module, exports) => {

const mod = __turbopack_context__.x("http", () => require("http"));

module.exports = mod;
}),
"[externals]/https [external] (https, cjs)", ((__turbopack_context__, module, exports) => {

const mod = __turbopack_context__.x("https", () => require("https"));

module.exports = mod;
}),
"[externals]/url [external] (url, cjs)", ((__turbopack_context__, module, exports) => {

const mod = __turbopack_context__.x("url", () => require("url"));

module.exports = mod;
}),
"[externals]/fs [external] (fs, cjs)", ((__turbopack_context__, module, exports) => {

const mod = __turbopack_context__.x("fs", () => require("fs"));

module.exports = mod;
}),
"[externals]/crypto [external] (crypto, cjs)", ((__turbopack_context__, module, exports) => {

const mod = __turbopack_context__.x("crypto", () => require("crypto"));

module.exports = mod;
}),
"[externals]/http2 [external] (http2, cjs)", ((__turbopack_context__, module, exports) => {

const mod = __turbopack_context__.x("http2", () => require("http2"));

module.exports = mod;
}),
"[externals]/assert [external] (assert, cjs)", ((__turbopack_context__, module, exports) => {

const mod = __turbopack_context__.x("assert", () => require("assert"));

module.exports = mod;
}),
"[externals]/tty [external] (tty, cjs)", ((__turbopack_context__, module, exports) => {

const mod = __turbopack_context__.x("tty", () => require("tty"));

module.exports = mod;
}),
"[externals]/os [external] (os, cjs)", ((__turbopack_context__, module, exports) => {

const mod = __turbopack_context__.x("os", () => require("os"));

module.exports = mod;
}),
"[externals]/zlib [external] (zlib, cjs)", ((__turbopack_context__, module, exports) => {

const mod = __turbopack_context__.x("zlib", () => require("zlib"));

module.exports = mod;
}),
"[externals]/events [external] (events, cjs)", ((__turbopack_context__, module, exports) => {

const mod = __turbopack_context__.x("events", () => require("events"));

module.exports = mod;
}),
"[project]/frontend/src/app/utils/api.ts [app-ssr] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "apiClient",
    ()=>apiClient,
    "createComment",
    ()=>createComment,
    "createDefect",
    ()=>createDefect,
    "createProject",
    ()=>createProject,
    "deleteAttachment",
    ()=>deleteAttachment,
    "deleteDefect",
    ()=>deleteDefect,
    "deleteProject",
    ()=>deleteProject,
    "exportDefectsToCsvExcel",
    ()=>exportDefectsToCsvExcel,
    "fetchAnalyticsSummary",
    ()=>fetchAnalyticsSummary,
    "fetchAttachmentsForDefect",
    ()=>fetchAttachmentsForDefect,
    "fetchCommentsForDefect",
    ()=>fetchCommentsForDefect,
    "fetchCreationTrend",
    ()=>fetchCreationTrend,
    "fetchCurrentUser",
    ()=>fetchCurrentUser,
    "fetchDefectById",
    ()=>fetchDefectById,
    "fetchDefects",
    ()=>fetchDefects,
    "fetchPriorityDistribution",
    ()=>fetchPriorityDistribution,
    "fetchProjectById",
    ()=>fetchProjectById,
    "fetchProjectPerformance",
    ()=>fetchProjectPerformance,
    "fetchProjects",
    ()=>fetchProjects,
    "fetchStatusDistribution",
    ()=>fetchStatusDistribution,
    "fetchUsers",
    ()=>fetchUsers,
    "loginUser",
    ()=>loginUser,
    "registerUser",
    ()=>registerUser,
    "updateDefect",
    ()=>updateDefect,
    "updateProject",
    ()=>updateProject,
    "updateUserRole",
    ()=>updateUserRole,
    "uploadAttachment",
    ()=>uploadAttachment
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$frontend$2f$node_modules$2f$axios$2f$lib$2f$axios$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/frontend/node_modules/axios/lib/axios.js [app-ssr] (ecmascript)");
;
const API_BASE_URL = ("TURBOPACK compile-time value", "http://localhost:8000") || 'http://localhost:8000';
const apiClient = __TURBOPACK__imported__module__$5b$project$5d2f$frontend$2f$node_modules$2f$axios$2f$lib$2f$axios$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["default"].create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json'
    }
});
const loginUser = async (userData)=>{
    const response = await apiClient.post('/token', new URLSearchParams({
        username: userData.username,
        password: userData.password
    }), {
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    });
    return response.data;
};
const registerUser = async (userData)=>{
    const response = await apiClient.post('/register/', userData);
    return response.data;
};
const fetchCurrentUser = async (token)=>{
    const response = await apiClient.get('/users/me/', {
        headers: {
            Authorization: `Bearer ${token}`
        }
    });
    return response.data;
};
const createProject = async (token, userId, projectData)=>{
    const response = await apiClient.post(`/users/${userId}/projects/`, projectData, {
        headers: {
            Authorization: `Bearer ${token}`
        }
    });
    return response.data;
};
const updateProject = async (token, projectId, projectData)=>{
    const response = await apiClient.put(`/projects/${projectId}`, projectData, {
        headers: {
            Authorization: `Bearer ${token}`
        }
    });
    return response.data;
};
const deleteProject = async (token, projectId)=>{
    await apiClient.delete(`/projects/${projectId}`, {
        headers: {
            Authorization: `Bearer ${token}`
        }
    });
};
const fetchProjectById = async (token, projectId)=>{
    const response = await apiClient.get(`/projects/${projectId}`, {
        headers: {
            Authorization: `Bearer ${token}`
        }
    });
    return response.data;
};
const fetchDefectById = async (token, defectId)=>{
    const response = await apiClient.get(`/defects/${defectId}`, {
        headers: {
            Authorization: `Bearer ${token}`
        }
    });
    return response.data;
};
const fetchProjects = async (token)=>{
    const response = await apiClient.get('/projects/', {
        headers: {
            Authorization: `Bearer ${token}`
        }
    });
    return response.data;
};
const fetchDefects = async (token)=>{
    const response = await apiClient.get('/defects/', {
        headers: {
            Authorization: `Bearer ${token}`
        }
    });
    return response.data;
};
const createDefect = async (token, defectData)=>{
    const response = await apiClient.post('/defects/', defectData, {
        headers: {
            Authorization: `Bearer ${token}`
        }
    });
    return response.data;
};
const updateDefect = async (token, defectId, defectData)=>{
    const response = await apiClient.put(`/defects/${defectId}`, defectData, {
        headers: {
            Authorization: `Bearer ${token}`
        }
    });
    return response.data;
};
const deleteDefect = async (token, defectId)=>{
    await apiClient.delete(`/defects/${defectId}`, {
        headers: {
            Authorization: `Bearer ${token}`
        }
    });
};
const fetchCommentsForDefect = async (token, defectId)=>{
    const response = await apiClient.get(`/defects/${defectId}/comments/`, {
        headers: {
            Authorization: `Bearer ${token}`
        }
    });
    return response.data;
};
const createComment = async (token, defectId, commentData)=>{
    const response = await apiClient.post(`/defects/${defectId}/comments/`, commentData, {
        headers: {
            Authorization: `Bearer ${token}`
        }
    });
    return response.data;
};
const fetchAttachmentsForDefect = async (token, defectId)=>{
    const response = await apiClient.get(`/defects/${defectId}/attachments/`, {
        headers: {
            Authorization: `Bearer ${token}`
        }
    });
    return response.data;
};
const uploadAttachment = async (token, defectId, file)=>{
    const formData = new FormData();
    formData.append('file', file);
    const response = await apiClient.post(`/defects/${defectId}/attachments/`, formData, {
        headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'multipart/form-data'
        }
    });
    return response.data;
};
const deleteAttachment = async (token, defectId, attachmentId)=>{
    await apiClient.delete(`/defects/${defectId}/attachments/${attachmentId}`, {
        headers: {
            Authorization: `Bearer ${token}`
        }
    });
};
const fetchUsers = async (token)=>{
    const response = await apiClient.get('/admin/users/', {
        headers: {
            Authorization: `Bearer ${token}`
        }
    });
    return response.data;
};
const updateUserRole = async (token, userId, newRole)=>{
    const response = await apiClient.put(`/users/${userId}/role`, {
        new_role: newRole
    }, {
        headers: {
            Authorization: `Bearer ${token}`
        }
    });
    return response.data;
};
const exportDefectsToCsvExcel = async (token, format, filters)=>{
    const response = await apiClient.get('/reports/defects/export', {
        headers: {
            Authorization: `Bearer ${token}`
        },
        params: {
            format,
            ...filters
        },
        responseType: 'blob'
    });
    return response.data;
};
const fetchAnalyticsSummary = async (token, startDate, endDate)=>{
    const params = {
        start_date: startDate,
        end_date: endDate
    };
    const response = await apiClient.get('/reports/analytics/summary', {
        headers: {
            Authorization: `Bearer ${token}`
        },
        params: params
    });
    return response.data;
};
const fetchStatusDistribution = async (token, startDate, endDate)=>{
    const params = {
        start_date: startDate,
        end_date: endDate
    };
    const response = await apiClient.get('/reports/analytics/status-distribution', {
        headers: {
            Authorization: `Bearer ${token}`
        },
        params: params
    });
    return response.data;
};
const fetchPriorityDistribution = async (token, startDate, endDate)=>{
    const params = {
        start_date: startDate,
        end_date: endDate
    };
    const response = await apiClient.get('/reports/analytics/priority-distribution', {
        headers: {
            Authorization: `Bearer ${token}`
        },
        params: params
    });
    return response.data;
};
const fetchCreationTrend = async (token, days = 30)=>{
    const params = {
        days: days
    };
    const response = await apiClient.get('/reports/analytics/creation-trend', {
        headers: {
            Authorization: `Bearer ${token}`
        },
        params: params
    });
    return response.data;
};
const fetchProjectPerformance = async (token, startDate, endDate)=>{
    const params = {
        start_date: startDate,
        end_date: endDate
    };
    const response = await apiClient.get('/reports/analytics/project-performance', {
        headers: {
            Authorization: `Bearer ${token}`
        },
        params: params
    });
    return response.data;
};
// Добавляем интерцептор для автоматического добавления токена к запросам
apiClient.interceptors.request.use((config)=>{
    const token = localStorage.getItem('access_token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
}, (error)=>{
    return Promise.reject(error);
});
apiClient.interceptors.response.use((response)=>response, (error)=>{
    if (error.response) {
        // Сервер ответил со статусом, отличным от 2xx
        console.error('API Error Response Data:', JSON.stringify(error.response.data, null, 2));
        console.error('API Error Status:', error.response.status);
        console.error('API Error Headers:', error.response.headers);
    } else if (error.request) {
        // Запрос был сделан, но ответа не получено
        console.error('API Error Request:', error.request);
    } else {
        // Что-то пошло не так при настройке запроса
        console.error('Error Message:', error.message);
    }
    return Promise.reject(error);
});
}),
"[project]/frontend/src/app/context/AuthContext.tsx [app-ssr] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "AuthProvider",
    ()=>AuthProvider,
    "useAuth",
    ()=>useAuth
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$frontend$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/frontend/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react-jsx-dev-runtime.js [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$frontend$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/frontend/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react.js [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$frontend$2f$node_modules$2f$next$2f$navigation$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/frontend/node_modules/next/navigation.js [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$frontend$2f$src$2f$app$2f$utils$2f$api$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/frontend/src/app/utils/api.ts [app-ssr] (ecmascript)");
'use client';
;
;
;
;
const AuthContext = /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$frontend$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["createContext"])(undefined);
const AuthProvider = ({ children })=>{
    const [user, setUser] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$frontend$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])(null);
    const [token, setToken] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$frontend$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])(null);
    const [isLoading, setIsLoading] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$frontend$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])(true);
    const router = (0, __TURBOPACK__imported__module__$5b$project$5d2f$frontend$2f$node_modules$2f$next$2f$navigation$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useRouter"])();
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$frontend$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useEffect"])(()=>{
        const loadUserFromStorage = async ()=>{
            try {
                const storedToken = localStorage.getItem('access_token');
                if (storedToken) {
                    setToken(storedToken);
                    const fetchedUser = await (0, __TURBOPACK__imported__module__$5b$project$5d2f$frontend$2f$src$2f$app$2f$utils$2f$api$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["fetchCurrentUser"])(storedToken);
                    setUser(fetchedUser);
                }
            } catch (error) {
                console.error('Failed to load user from storage:', error);
                logout(); // Выходим, если токен недействителен или ошибка
            } finally{
                setIsLoading(false);
            }
        };
        loadUserFromStorage();
    }, []);
    const login = async (username, password)=>{
        setIsLoading(true);
        try {
            const response = await (0, __TURBOPACK__imported__module__$5b$project$5d2f$frontend$2f$src$2f$app$2f$utils$2f$api$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["loginUser"])({
                username,
                password
            });
            setToken(response.access_token);
            localStorage.setItem('access_token', response.access_token);
            const fetchedUser = await (0, __TURBOPACK__imported__module__$5b$project$5d2f$frontend$2f$src$2f$app$2f$utils$2f$api$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["fetchCurrentUser"])(response.access_token);
            setUser(fetchedUser);
            router.push('/');
        } catch (error) {
            console.error('Login failed:', error);
            throw error;
        } finally{
            setIsLoading(false);
        }
    };
    const register = async (userData)=>{
        setIsLoading(true);
        try {
            // На бэкенде роль принудительно устанавливается в "observer"
            const newUser = await (0, __TURBOPACK__imported__module__$5b$project$5d2f$frontend$2f$src$2f$app$2f$utils$2f$api$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["registerUser"])({
                ...userData,
                role: "observer"
            });
            router.push('/login');
            return newUser;
        } catch (error) {
            console.error('Registration failed:', error);
            throw error;
        } finally{
            setIsLoading(false);
        }
    };
    const logout = ()=>{
        setToken(null);
        setUser(null);
        localStorage.removeItem('access_token');
        router.push('/login');
    };
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$frontend$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(AuthContext.Provider, {
        value: {
            user,
            token,
            login,
            register,
            logout,
            isLoading
        },
        children: children
    }, void 0, false, {
        fileName: "[project]/frontend/src/app/context/AuthContext.tsx",
        lineNumber: 86,
        columnNumber: 5
    }, ("TURBOPACK compile-time value", void 0));
};
const useAuth = ()=>{
    const context = (0, __TURBOPACK__imported__module__$5b$project$5d2f$frontend$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useContext"])(AuthContext);
    if (context === undefined) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
};
}),
"[project]/frontend/src/app/components/ClientHeaderWrapper.tsx [app-ssr] (ecmascript)", ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s([
    "default",
    ()=>__TURBOPACK__default__export__
]);
var __TURBOPACK__imported__module__$5b$project$5d2f$frontend$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/frontend/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react-jsx-dev-runtime.js [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$frontend$2f$node_modules$2f$next$2f$dist$2f$shared$2f$lib$2f$app$2d$dynamic$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/frontend/node_modules/next/dist/shared/lib/app-dynamic.js [app-ssr] (ecmascript)");
;
'use client';
;
;
const Header = (0, __TURBOPACK__imported__module__$5b$project$5d2f$frontend$2f$node_modules$2f$next$2f$dist$2f$shared$2f$lib$2f$app$2d$dynamic$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["default"])(async ()=>{}, {
    loadableGenerated: {
        modules: [
            "[project]/frontend/src/app/components/Header.tsx [app-client] (ecmascript, next/dynamic entry)"
        ]
    },
    ssr: false
});
const ClientHeaderWrapper = ()=>{
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$frontend$2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(Header, {}, void 0, false, {
        fileName: "[project]/frontend/src/app/components/ClientHeaderWrapper.tsx",
        lineNumber: 8,
        columnNumber: 10
    }, ("TURBOPACK compile-time value", void 0));
};
const __TURBOPACK__default__export__ = ClientHeaderWrapper;
}),
];

//# sourceMappingURL=%5Broot-of-the-server%5D__df554707._.js.map
import { useState, useEffect } from "react";
import axios from "axios";

// Sample network connections for testing
const samples = {
  normal: {
    duration: 0,
    protocol_type: "tcp",
    service: "http",
    flag: "SF",
    src_bytes: 181,
    dst_bytes: 5450,
    land: 0,
    wrong_fragment: 0,
    urgent: 0,
    hot: 0,
    num_failed_logins: 0,
    logged_in: 1,
    num_compromised: 0,
    root_shell: 0,
    su_attempted: 0,
    num_root: 0,
    num_file_creations: 0,
    num_shells: 0,
    num_access_files: 0,
    num_outbound_cmds: 0,
    is_host_login: 0,
    is_guest_login: 0,
    count: 9,
    srv_count: 9,
    serror_rate: 0.0,
    srv_serror_rate: 0.0,
    rerror_rate: 0.0,
    srv_rerror_rate: 0.0,
    same_srv_rate: 1.0,
    diff_srv_rate: 0.0,
    srv_diff_host_rate: 0.0,
    dst_host_count: 9,
    dst_host_srv_count: 9,
    dst_host_same_srv_rate: 1.0,
    dst_host_diff_srv_rate: 0.0,
    dst_host_same_src_port_rate: 1.0,
    dst_host_srv_diff_host_rate: 0.0,
    dst_host_serror_rate: 0.0,
    dst_host_srv_serror_rate: 0.0,
    dst_host_rerror_rate: 0.0,
    dst_host_srv_rerror_rate: 0.0,
  },
  attack: {
      duration: 0,
      protocol_type: "icmp",
      service: "ecr_i",
      flag: "SF",
      src_bytes: 1032,
      dst_bytes: 0,
      land: 0,
      wrong_fragment: 0,
      urgent: 0,
      hot: 0,
      num_failed_logins: 0,
      logged_in: 0,
      num_compromised: 0,
      root_shell: 0,
      su_attempted: 0,
      num_root: 0,
      num_file_creations: 0,
      num_shells: 0,
      num_access_files: 0,
      num_outbound_cmds: 0,
      is_host_login: 0,
      is_guest_login: 0,
      count: 511,
      srv_count: 511,
      serror_rate: 0.0,
      srv_serror_rate: 0.0,
      rerror_rate: 0.0,
      srv_rerror_rate: 0.0,
      same_srv_rate: 1.0,
      diff_srv_rate: 0.0,
      srv_diff_host_rate: 0.0,
      dst_host_count: 255,
      dst_host_srv_count: 110,
      dst_host_same_srv_rate: 0.43,
      dst_host_diff_srv_rate: 0.02,
      dst_host_same_src_port_rate: 0.43,
      dst_host_srv_diff_host_rate: 0.0,
      dst_host_serror_rate: 0.01,
      dst_host_srv_serror_rate: 0.0,
      dst_host_rerror_rate: 0.02,
      dst_host_srv_rerror_rate: 0.0,
  },
  custom: {}, // Will be filled with a copy of normal sample for customization
};

// API URL - can be configured for different environments
const API_URL = "http://localhost:8000";

function App() {
  const [selected, setSelected] = useState("normal");
  const [prediction, setPrediction] = useState(null);
  const [probability, setProbability] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [customData, setCustomData] = useState({});
  const [useCustom, setUseCustom] = useState(false);
  const [modelInfo, setModelInfo] = useState(null);
  const [apiStatus, setApiStatus] = useState("unknown");

  // Initialize custom data with normal sample
  useEffect(() => {
    setCustomData({ ...samples.normal });
  }, []);

  // Check API status on component mount
  useEffect(() => {
    checkApiStatus();
  }, []);

  // Function to fetch model information
  const fetchModelInfo = async () => {
    try {
      const res = await axios.get(`${API_URL}/model_info`);
      setModelInfo(res.data);
    } catch (err) {
      console.error("Error fetching model info:", err);
    }
  };

  // Check if API is available
  const checkApiStatus = async () => {
    try {
      await axios.get(`${API_URL}`);
      setApiStatus("online");
      // If API is online, fetch model info
      fetchModelInfo();
    } catch (err) {
      setApiStatus("offline");
    }
  };

  // Handle predict button click
  const handlePredict = async () => {
    setLoading(true);
    setPrediction(null);
    setProbability(null);
    setError(null);

    try {
      // Determine which data to send
      const dataToSend = useCustom ? customData : samples[selected];

      const res = await axios.post(`${API_URL}/predict`, dataToSend);
      console.log(res);
      setPrediction(res.data.prediction);
      setProbability(res.data.probabilities);
    } catch (err) {
      console.error("API error:", err);
      setError(
        err.response?.data?.detail ||
          "Lỗi khi gọi API. Vui lòng kiểm tra kết nối."
      );
    } finally {
      setLoading(false);
    }
  };

  // Handle custom data changes
  const handleCustomDataChange = (field, value) => {
    setCustomData({
      ...customData,
      [field]: parseFloat(value) || 0,
    });
  };

  // Handle radio button change
  const handleRadioChange = (e) => {
    if (e.target.value === "custom") {
      setUseCustom(true);
    } else {
      setUseCustom(false);
      setSelected(e.target.value);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center justify-center p-6">
      <div className="bg-white p-8 rounded-2xl shadow-lg w-full max-w-2xl">
        <h1 className="text-3xl font-bold mb-6 text-center text-blue-800">
          Hệ Thống Phát Hiện Tấn Công Mạng
        </h1>

        {/* API Status Indicator */}
        <div className="mb-6 flex items-center justify-center">
          <span className="mr-2">Trạng thái API:</span>
          <span
            className={`px-2 py-1 rounded-full text-sm font-medium ${
              apiStatus === "online"
                ? "bg-green-100 text-green-800"
                : apiStatus === "offline"
                ? "bg-red-100 text-red-800"
                : "bg-yellow-100 text-yellow-800"
            }`}
          >
            {apiStatus === "online"
              ? "Trực tuyến"
              : apiStatus === "offline"
              ? "Ngoại tuyến"
              : "Kiểm tra..."}
          </span>
          {apiStatus === "offline" && (
            <button
              onClick={checkApiStatus}
              className="ml-2 text-sm text-blue-600 hover:text-blue-800"
            >
              Thử lại
            </button>
          )}
        </div>

        {/* Sample Selection */}
        <div className="mb-6">
          <h2 className="text-lg font-semibold mb-3">Chọn mẫu dữ liệu:</h2>
          <div className="space-y-2">
            <label className="flex items-center space-x-2">
              <input
                type="radio"
                value="normal"
                checked={!useCustom && selected === "normal"}
                onChange={handleRadioChange}
                className="form-radio h-5 w-5 text-blue-600"
              />
              <span>Mẫu NORMAL (bình thường)</span>
            </label>
            <label className="flex items-center space-x-2">
              <input
                type="radio"
                value="attack"
                checked={!useCustom && selected === "attack"}
                onChange={handleRadioChange}
                className="form-radio h-5 w-5 text-blue-600"
              />
              <span>Mẫu ATTACK (tấn công)</span>
            </label>
            <label className="flex items-center space-x-2">
              <input
                type="radio"
                value="custom"
                checked={useCustom}
                onChange={handleRadioChange}
                className="form-radio h-5 w-5 text-blue-600"
              />
              <span>Tùy chỉnh</span>
            </label>
          </div>
        </div>

        {/* Custom Data Inputs - show only when custom is selected */}
        {useCustom && modelInfo && (
          <div className="mb-6">
            <h2 className="text-lg font-semibold mb-3">
              Tùy chỉnh các đặc trưng quan trọng:
            </h2>
            <div className="grid grid-cols-2 gap-4">
              {modelInfo.top_features.map((feature) => (
                <div key={feature} className="mb-2">
                  <label className="block text-sm font-medium text-gray-700">
                    {feature}:
                  </label>
                  <input
                    type="number"
                    className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                    value={customData[feature] || 0}
                    onChange={(e) =>
                      handleCustomDataChange(feature, e.target.value)
                    }
                  />
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Submit Button */}
        <div className="text-center mb-6">
          <button
            className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition font-medium text-lg disabled:opacity-50"
            onClick={handlePredict}
            disabled={loading || apiStatus !== "online"}
          >
            {loading ? "Đang xử lý..." : "Phân tích kết nối"}
          </button>
        </div>

        {/* Error Message */}
        {error && (
          <div className="p-4 mb-6 bg-red-50 border border-red-200 rounded-lg text-red-700">
            <p className="font-medium">Lỗi:</p>
            <p>{error}</p>
          </div>
        )}

        {/* Prediction Result */}
        {prediction && (
          <div className="p-6 bg-gray-50 rounded-lg border shadow-sm">
            <h2 className="text-xl font-bold mb-4 text-center">
              Kết quả phân tích
            </h2>
            <div className="flex justify-between items-center">
              <div className="text-lg">
                <span className="font-medium">Phân loại:</span>{" "}
                <span
                  className={`font-bold ${
                    prediction === "normal" ? "text-green-600" : "text-red-600"
                  }`}
                >
                  {prediction === "normal" ? "BÌNH THƯỜNG" : "TẤN CÔNG"}
                </span>
              </div>

              {probability !== null && (
                <div className="text-lg">
                  <span className="font-medium">Độ tin cậy:</span>{" "}
                  <span className="font-bold">
                    {probability.attack > probability.normal
                      ? (probability.attack * 100).toFixed(2)
                      : (probability.normal * 100).toFixed(2)}
                    %
                  </span>
                </div>
              )}
            </div>

            {prediction === "attack" && (
              <div className="mt-4 p-3 bg-red-50 text-red-700 rounded border border-red-200">
                <p className="font-medium">⚠️ Cảnh báo:</p>
                <p>Phát hiện dấu hiệu tấn công mạng trong kết nối này!</p>
              </div>
            )}
          </div>
        )}

        {/* Model Information */}
        {modelInfo && (
          <div className="mt-8 text-sm text-gray-600">
            <p className="font-medium">Thông tin mô hình:</p>
            <p>Loại: {modelInfo.model_type}</p>
            <p>Số đặc trưng: {modelInfo.total_features}</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;

import { useState, useEffect, useMemo } from "react";
import client from "../api/client";
import Select from "react-select";
import { Mic, Search } from "lucide-react";
import { useDispatch, useSelector } from "react-redux";
import { clearExtractedData } from "../features/interaction/interactionSlice";

export default function InteractionForm() {
  const [hcps, setHcps] = useState([]);

  const [form, setForm] = useState({
    hcp_id: "",
    meeting_type: "Meeting",
    date: "",
    time: "",
    attendees: "",
    discussion: "",
    summary: "",
    status: "Pending",
  });

  const dispatch = useDispatch();

  const extractedData = useSelector(
    (state) => state.interaction?.extractedData
  );

  useEffect(() => {
    const fetchHCPs = async () => {
      try {
        const res = await client.get("/hcps/");
        setHcps(res.data);
      } catch (err) {
        console.error(err);
      }
    };

    fetchHCPs();
  }, []);

  useEffect(() => {
    if (!extractedData || hcps.length === 0) return;

    setForm(prev => {
      let updated = {
        ...prev,
        ...extractedData,
      };

      // Fix time format for <input type="time"> (needs 24-hour HH:mm)
      if (updated.time) {
        // match "10:30 AM", "3 PM", "14:00"
        const timeMatch = String(updated.time).match(/(\d{1,2})(?::(\d{2}))?\s*(AM|PM)?/i);
        if (timeMatch) {
          let hours = parseInt(timeMatch[1], 10);
          const minutes = timeMatch[2] || "00";
          const period = timeMatch[3]?.toUpperCase();
          
          if (period === "PM" && hours < 12) hours += 12;
          if (period === "AM" && hours === 12) hours = 0;
          
          updated.time = `${hours.toString().padStart(2, "0")}:${minutes}`;
        }
      }

      // Map meeting_type to the strict select options
      if (updated.meeting_type) {
        const t = String(updated.meeting_type).toLowerCase();
        if (t.includes("virtual") || t.includes("zoom") || t.includes("teams")) {
          updated.meeting_type = "Virtual";
        } else if (t.includes("email")) {
          updated.meeting_type = "Email";
        } else if (t.includes("phone") || t.includes("call")) {
          updated.meeting_type = "Phone";
        } else {
          updated.meeting_type = "Meeting";
        }
      }

      if (
        extractedData.hcp_name &&
        typeof extractedData.hcp_name === "string"
      ) {
        const normalize = (name = "") =>
          name
            .toLowerCase()
            .replace(/^dr\.?\s*/i, "")
            .replace(/\./g, "")
            .trim();

        const aiName = normalize(extractedData.hcp_name);

        const matched = hcps.find((hcp) => {
          const dbName = normalize(hcp.name);
          return (
            dbName === aiName ||
            dbName.includes(aiName) ||
            aiName.includes(dbName)
          );
        });

        if (matched) {
          updated.hcp_id = matched.id;

          setTimeout(() => {
            dispatch(clearExtractedData());
          }, 200);
        }

        delete updated.hcp_name;
      }

      return updated;
    });

  }, [extractedData, hcps, dispatch]);

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]:
        e.target.type === "checkbox"
          ? e.target.checked
          : e.target.value,
    });
  };

  const hcpOptions = useMemo(
    () =>
      hcps.map((hcp) => ({
        value: hcp.id,
        label: `${hcp.name} • ${hcp.specialization} • ${hcp.hospital}`,
      })),
    [hcps]
  );

  const selectedOption = useMemo(() => {
    return (
      hcpOptions.find(
        option => String(option.value) === String(form.hcp_id)
      ) || null
    );
  }, [hcpOptions, form.hcp_id]);

  const submit = async (e) => {
    e.preventDefault();

    if (!form.hcp_id) {
      alert("Please select an HCP.");
      return;
    }

    if (!form.discussion.trim()) {
      alert("Discussion cannot be empty.");
      return;
    }

    try {
      await client.post("/interactions/", {
        hcp_id: form.hcp_id,
        meeting_type: form.meeting_type,
        discussion: form.discussion,
        summary: form.summary,
        follow_up_date: form.date,
        status: form.status,
      });

      alert("Interaction Logged");

      setForm({
        hcp_id: "",
        meeting_type: "Meeting",
        date: "",
        time: "",
        attendees: "",
        discussion: "",
        summary: "",
        status: "Pending",
      });
    } catch (err) {
      console.error(err);
      alert("Failed");
    }
  };

  const inputClass =
    "w-full h-[44px] rounded-md border border-[#d6d9de] bg-white px-3 text-[13px] text-[#3f3f46] outline-none transition-all duration-150 focus:border-[#2563EB] focus:ring-2 focus:ring-[#dbeafe]";

  return (
    <div className="w-full max-w-[900px]">

      <h1 className="text-[28px] font-semibold text-[#202124] mb-8">
        Log HCP Interaction
      </h1>

      <form
        onSubmit={submit}
      >

        <section>

          <h2 className="text-[13px] font-semibold text-[#444] mb-5">
            Interaction Details
          </h2>

          <div className="grid grid-cols-2 gap-8">

            <div>

              <label className="block mb-2 text-[13px] font-medium text-[#4b5563]">
                HCP Name
              </label>

              <Select
                value={selectedOption}
                options={hcpOptions}
                isDisabled
                placeholder="Waiting for AI..."
              />

            </div>

            <div>

              <label className="block mb-2 text-[13px] font-medium text-[#4b5563]">
                Interaction Type
              </label>

              <select
                name="meeting_type"
                value={form.meeting_type}
                onChange={handleChange}
                className={inputClass}
              >
                <option>Meeting</option>
                <option>Virtual</option>
                <option>Email</option>
                <option>Phone</option>
              </select>

            </div>

          </div>

          <div className="grid grid-cols-2 gap-8 mt-6">

            <div>

              <label className="block mb-2 text-[13px] font-medium text-[#4b5563]">
                Date
              </label>

              <input
                type="date"
                name="date"
                value={form.date}
                onChange={handleChange}
                autoComplete="off"
                className={inputClass}
              />

            </div>

            <div>

              <label className="block mb-2 text-[13px] font-medium text-[#4b5563]">
                Time
              </label>

              <input
                type="time"
                name="time"
                value={form.time}
                onChange={handleChange}
                autoComplete="off"
                className={inputClass}
              />

            </div>

          </div>

        </section>
        <section className="mt-10">

          <div>

            <label className="block mb-2 text-[13px] font-medium text-[#4b5563]">
              Attendees
            </label>

            <input
              type="text"
              name="attendees"
              value={form.attendees}
              onChange={handleChange}
              placeholder="Enter names or search..."
              autoComplete="off"
              className={inputClass}
            />

          </div>

        </section>

        {/* Topics Discussed */}

        <section className="mt-10">

          <div>

            <label className="block mb-2 text-[13px] font-medium text-[#4b5563]">
              Topics Discussed
            </label>

            <textarea
              name="discussion"
              value={form.discussion}
              onChange={handleChange}
              rows={6}
              placeholder="Enter key discussion points..."
              className="w-full rounded-md border border-[#d9d9d9] bg-white p-3 text-[13px] text-[#444] outline-none resize-none transition-all duration-150 focus:border-[#2563EB] focus:ring-2 focus:ring-blue-100"
            />

          </div>

        </section>

        {/* Summary */}

        <section className="mt-10">

          <div>

            <label className="block mb-2 text-[13px] font-medium text-[#4b5563]">
              Summary
            </label>

            <textarea
              name="summary"
              value={form.summary}
              onChange={handleChange}
              rows={3}
              placeholder="Brief summary..."
              className="w-full rounded-md border border-[#d9d9d9] bg-white p-3 text-[13px] text-[#444] outline-none resize-none transition-all duration-150 focus:border-[#2563EB] focus:ring-2 focus:ring-blue-100"
            />

          </div>

        </section>

        {/* Bottom Buttons */}

        <div className="flex justify-end gap-3 pt-2 mt-10">

          <button
            type="button"
            onClick={() =>
              setForm({
                hcp_id: "",
                meeting_type: "Meeting",
                date: "",
                time: "",
                attendees: "",
                discussion: "",
                summary: "",
                status: "Pending",
              })
            }
            className="px-6 h-11 rounded-md border border-[#d9d9d9] bg-white text-[13px] font-medium text-[#555] hover:bg-gray-50"
          >
            Cancel
          </button>

          <button
            type="submit"
            className="px-8 h-11 rounded-lg bg-[#0052FF] hover:bg-[#0048e6] text-white text-[13px] font-semibold shadow-sm transition-colors"
          >
            Log Interaction
          </button>

        </div>

      </form>

    </div>
  );
}
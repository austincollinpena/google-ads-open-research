import React from "react";
import { useState, useRef } from "react";

function classNames(...classes: string[]) {
  return classes.filter(Boolean).join(" ");
}

export default function NGramUploader() {
  const [isROASTarget, setIsROASTarget] = useState(true);
  const [email, setEmail] = useState("");
  const [target, setTarget] = useState<number | string>("");
  const [file, setFile] = useState<undefined | File>(undefined);
  const [loading, setLoading] = useState(false);
  const formRef = useRef<null | HTMLFormElement>(null);
  const [success, setSuccess] = useState(false);

  const handleSubmit = async (e: any) => {
    e.preventDefault();
    if (!formRef || !file) {
      return;
    }

    const valid = formRef.current?.reportValidity();
    if (!valid) {
      return;
    }
    if (target === 0) {
      window.alert("please set a target ROAS or CPA");
      return;
    }
    setLoading(true);
    const formData = new FormData();
    const formBody = {
      email: email,
      target: target,
      isROASTarget: isROASTarget,
    };
    formData.append("args", JSON.stringify(formBody));
    formData.append("csvData", file);
    try {
      fetch(`${import.meta.env.PUBLIC_PUBLIC_API}/v1/api/free-tools/ngram`, {
        method: "POST",
        body: formData,
        credentials: "include",
      })
        .then((r) => {
          if (!r.ok || [400, 401, 402, 403, 404, 500].includes(r.status)) {
            r.json().then((v) => window.alert(v["error_message"]));
            console.log();
            setLoading(false);
            setSuccess(true);
            // @ts-ignore clear the HTML file cache
            document.querySelector("#upload-file").value = null;
          } else {
            setEmail("");
            setTarget("");
            setFile(undefined);
            // @ts-ignore clear the HTML file cache
            document.querySelector("#upload-file").value = null;
            setLoading(false);
            setSuccess(true);
          }
        })
        .catch((e) => {
          window.alert(e);
          setLoading(false);
          setSuccess(false);
        });
    } catch (e) {
      setLoading(false);
      window.alert("something went wrong, please contact us");
    }
  };

  return (
    <div className="max-w-[1200px] mx-auto mb-8">
      <form
        ref={formRef}
        onSubmit={(e) => handleSubmit(e)}
        className="space-y-6"
      >
        <div className="bg-[#F6E9DD] border-4 border-black px-4 py-5 shadow  sm:p-6">
          <div className="md:grid md:grid-cols-3 md:gap-6">
            <div className="md:col-span-1">
              <h3 className="text-lg font-medium leading-6 text-gray-900">
                Upload your document here
              </h3>
              <p className="mt-1 text-sm text-gray-500">
                Your information is not stored, processed or used in any way
                other than to generate a report and send you an email.
              </p>
            </div>
            <div className="mt-5 space-y-6 md:col-span-2 md:mt-0">
              <div className="grid grid-cols-3 gap-6">
                <div className="col-span-3 sm:col-span-2">
                  <div>
                    <label
                      htmlFor="email"
                      className="block text-sm font-medium text-gray-700"
                    >
                      Email
                    </label>
                    <div className="mt-1">
                      <input
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        type="email"
                        name="email"
                        id="email"
                        className="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                        placeholder="you@example.com"
                        required
                      />
                    </div>
                  </div>
                </div>
              </div>
              <div>
                <div className="sm:hidden">
                  <label htmlFor="tabs" className="sr-only">
                    Select a tab
                  </label>
                </div>
                <div className="hidden sm:block">
                  <label
                    htmlFor="email"
                    className="block text-sm font-medium text-gray-700 mb-2"
                  >
                    If you don't have conversion value, choose "CPA Target"
                  </label>
                  <div
                    className="isolate flex divide-x divide-gray-200 rounded-lg shadow"
                    aria-label="Tabs"
                  >
                    <div
                      onClick={() => {
                        setIsROASTarget(true);
                      }}
                      className={classNames(
                        isROASTarget
                          ? "text-gray-900"
                          : "text-gray-500 hover:text-gray-700",
                        isROASTarget ? "rounded-l-lg" : "",
                        isROASTarget ? "rounded-r-lg" : "",
                        "group relative min-w-0 flex-1 overflow-hidden bg-white py-4 px-4 text-sm font-medium text-center hover:bg-gray-50 focus:z-10 cursor-pointer"
                      )}
                    >
                      <span>ROAS Target</span>
                      <span
                        aria-hidden="true"
                        className={classNames(
                          isROASTarget ? "bg-black" : "bg-transparent",
                          "absolute inset-x-0 bottom-0 h-0.5"
                        )}
                      />
                    </div>
                    <div
                      onClick={() => {
                        setIsROASTarget(false);
                      }}
                      className={classNames(
                        !isROASTarget
                          ? "text-gray-900"
                          : "text-gray-500 hover:text-gray-700",
                        !isROASTarget ? "rounded-l-lg" : "",
                        !isROASTarget ? "rounded-r-lg" : "",
                        "group relative min-w-0 flex-1 overflow-hidden bg-white py-4 px-4 text-sm font-medium text-center hover:bg-gray-50 focus:z-10 cursor-pointer"
                      )}
                    >
                      <span>CPA Target </span>
                      <span
                        aria-hidden="true"
                        className={classNames(
                          !isROASTarget ? "bg-black" : "bg-transparent",
                          "absolute inset-x-0 bottom-0 h-0.5"
                        )}
                      />
                    </div>
                  </div>
                </div>
              </div>
              <div className="grid grid-cols-3 gap-6">
                <div className="col-span-3 sm:col-span-2">
                  <div>
                    <label
                      htmlFor="target"
                      className="block text-sm font-medium text-gray-700"
                    >
                      {isROASTarget ? "ROAS Target" : "CPA Target"}
                    </label>
                    <div className="mt-1 relative">
                      <div className="absolute -left-4 top-2">
                        {!isROASTarget && "$"}
                      </div>
                      <input
                        value={target}
                        onChange={(e) => setTarget(parseFloat(e.target.value))}
                        type="number"
                        name="target"
                        step=".01"
                        required
                        id="target"
                        className="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                        placeholder={isROASTarget ? "5.5" : "54"}
                      />
                    </div>
                  </div>
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Upload your search term data
                </label>
                <label
                  htmlFor="upload-file"
                  className="mt-1 flex justify-center rounded-md border-2 border-dashed border-gray-300 px-6 pt-5 pb-6 cursor-pointer"
                  onClick={(e) => {
                    if (file) {
                      e.preventDefault();
                      // @ts-ignore clear the HTML file cache
                      document.querySelector("#upload-file").value = null;
                      setFile(undefined);
                    }
                  }}
                >
                  {file ? (
                    <p>Click to remove {file.name}</p>
                  ) : (
                    <div className="space-y-1 text-center">
                      <svg
                        className="mx-auto h-12 w-12 text-gray-400"
                        stroke="currentColor"
                        fill="none"
                        viewBox="0 0 48 48"
                        aria-hidden="true"
                      >
                        <path
                          d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02"
                          strokeWidth={2}
                          strokeLinecap="round"
                          strokeLinejoin="round"
                        />
                      </svg>
                      <div className="flex text-sm text-gray-600">
                        <span>Click Anywhere To Upload a file</span>

                        <p className="pl-1">or drag and drop</p>
                      </div>
                      <p className="text-xs text-gray-500">
                        .csv file required
                      </p>
                    </div>
                  )}
                  <input
                    accept={".csv"}
                    id="upload-file"
                    name="upload-file"
                    type="file"
                    className="sr-only"
                    required
                    onChange={(e) => {
                      if (!e.target.files) {
                        return;
                      }
                      setFile(e.target.files[0]);
                    }}
                  />
                </label>
              </div>
            </div>
          </div>
          <div className="flex justify-end mt-4">
            <button
              type="submit"
              disabled={loading}
              className={`ml-3
              ${loading && "opacity-70 cursor-wait"}
              inline-flex justify-center transition-opacity opacity-100 border border-transparent bg-black py-2 px-4 text-md mt-4 font-medium text-white shadow-sm hover:bg-stone-800 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2`}
            >
              Generate My Free N Gram Report
            </button>
          </div>
          {success && (
            <div className="mt-4 bg-green-50 border-4 border-black py-4 px-2 text-center">
              <p className="text-green-800">
                Success, your report is queued and will be sent to the email you
                provided. Depending on server load, this can take less than two
                minutes.
              </p>
            </div>
          )}
        </div>
      </form>
    </div>
  );
}

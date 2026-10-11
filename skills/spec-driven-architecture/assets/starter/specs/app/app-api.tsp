import "@typespec/http";

using TypeSpec.Http;

/**
 * Architecture: app.appApi.httpApi
 * Implementation: services/app/api.ts
 * Flow: specs/app/request-flow.mmd
 */
@doc("Sample public API. Replace this contract with the first real boundary.")
@service(#{ title: "App API" })
@server("http://localhost:8080", "Local")
namespace App.Api;

model Health {
  status: string;
}

@route("/health")
@get
op getHealth(): Health;

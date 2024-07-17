from fastapi import FastAPI
from fastapi_pagination import add_pagination
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource
from src.routers import api_router

trace.set_tracer_provider(
    TracerProvider(resource=Resource.create({"service.name": "workout-api"}))
)

tracer_provider = trace.get_tracer_provider()

jaeger_exporter = JaegerExporter(
    agent_host_name="jaeger",
    agent_port=6831,
)

tracer_provider.add_span_processor(BatchSpanProcessor(jaeger_exporter))

app = FastAPI(title="Workout API")

app.include_router(api_router)

add_pagination(app)

FastAPIInstrumentor.instrument_app(app)

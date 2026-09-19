from streamlit.testing.v1 import AppTest


def test_demo_runs_without_streamlit_exceptions():
    app = AppTest.from_file("../demo/app.py")
    app.run(timeout=30)
    assert len(app.exception) == 0
    assert app.title[0].value == "HAC - Horizon Agent Containment"
    assert "Action History" in [header.value for header in app.subheader]
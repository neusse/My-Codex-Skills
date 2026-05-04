from {{PACKAGE_NAME}}.main import main


def test_main_runs(capsys) -> None:
    main()
    captured = capsys.readouterr()
    assert "{{PROJECT_NAME}} is initialized." in captured.out

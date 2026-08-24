from app.main import greet, main


def test_greet():
    assert greet("Ada") == "Hello, Ada!"


def test_main_prints_greeting(capsys):
    main(["Ada"])
    captured = capsys.readouterr()
    assert captured.out.strip() == "Hello, Ada!"


def test_main_defaults_to_world(capsys):
    main([])
    captured = capsys.readouterr()
    assert captured.out.strip() == "Hello, world!"

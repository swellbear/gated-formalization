from options_offshoot.fields.catalog import (
    INDEX_MAP_DISCLAIMER,
    get_field,
    listed_field_ids,
    load_universe,
    menu_lines,
    this_friday,
)


def test_predeclared_three_fields():
    assert listed_field_ids() == [
        "earnings_us_week",
        "spx_this_friday",
        "index_only",
    ]
    assert get_field("index_only").allows_tickets is False
    assert get_field("spx_this_friday").allows_tickets is True


def test_menu_is_not_an_allocator():
    text = "\n".join(menu_lines())
    assert "PREDECLARED FIELDS" in text
    assert "fattest" in INDEX_MAP_DISCLAIMER.lower() or "shop" in INDEX_MAP_DISCLAIMER.lower()
    assert "Do not merge bankrolls" in text


def test_universe_files_load():
    spx = load_universe(get_field("spx_this_friday"))
    assert "AAPL" in spx
    assert load_universe(get_field("index_only")) == []
    from options_offshoot.fields.catalog import freeze_header

    meta = freeze_header(get_field("spx_this_friday"))
    assert meta["n"] == str(len(spx))
    assert "operator" in (meta.get("source") or "").lower() or meta.get("as_of")


def test_this_friday_is_friday():
    d = this_friday()
    assert d.weekday() == 4

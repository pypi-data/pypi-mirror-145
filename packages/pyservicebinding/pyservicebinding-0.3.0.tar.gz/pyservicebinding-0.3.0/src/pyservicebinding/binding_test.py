import pytest

from pyservicebinding import binding


def test_bindings(tmpdir, monkeypatch):
    bindings_dir = tmpdir.mkdir("bindings")
    junk = bindings_dir.join("junk")
    junk.write("junk text")
    sb1 = tmpdir.join("bindings").mkdir("sb1")
    sb1.mkdir("sub1")
    _type = sb1.join("type")
    _type.write("mysql")
    username = sb1.join("username")
    username.write("john")
    password = sb1.join("password")
    password.write("L&ia6W@n7epi18a")
    url = sb1.join("url")
    url.write("mysql://192.168.94.102:3306/school")

    sb2 = tmpdir.join("bindings").mkdir("sb2")
    _type = sb2.join("type")
    _type.write("neo4j")
    username = sb2.join("username")
    username.write("jane")
    password = sb2.join("password")
    password.write("o4%bGt#D8v2i0ja")
    uri = sb2.join("uri")
    uri.write("neo4j://192.168.94.103:7687/cr")

    monkeypatch.setenv("SERVICE_BINDING_ROOT", str(bindings_dir))

    sb = binding.ServiceBinding()
    l = sb.bindings("mysql")
    assert len(l) == 1
    b = l[0]
    assert b["username"] == "john"
    assert b["password"] == "L&ia6W@n7epi18a"
    assert b["url"] == "mysql://192.168.94.102:3306/school"

    l = sb.bindings("neo4j")
    assert len(l) == 1
    b = l[0]
    assert b["username"] == "jane"
    assert b["password"] == "o4%bGt#D8v2i0ja"
    assert b["uri"] == "neo4j://192.168.94.103:7687/cr"

    l = sb.bindings("non-existing")
    assert len(l) == 0

def test_bindings_with_provider(tmpdir, monkeypatch):
    bindings_dir = tmpdir.mkdir("bindings")
    sb1 = tmpdir.join("bindings").mkdir("sb1")
    _type = sb1.join("type")
    _type.write("mysql")
    provider = sb1.join("provider")
    provider.write("oracle")
    username = sb1.join("username")
    username.write("john")
    password = sb1.join("password")
    password.write("L&ia6W@n7epi18a")
    url = sb1.join("url")
    url.write("mysql://192.168.94.102:3306/school")

    sb2 = tmpdir.join("bindings").mkdir("sb2")
    _type = sb2.join("type")
    _type.write("mysql")
    provider = sb2.join("provider")
    provider.write("mariadb")
    username = sb2.join("username")
    username.write("jane")
    password = sb2.join("password")
    password.write("o4%bGt#D8v2i0ja")
    uri = sb2.join("uri")
    uri.write("mysql://192.168.94.103:7687/school")

    monkeypatch.setenv("SERVICE_BINDING_ROOT", str(bindings_dir))

    sb = binding.ServiceBinding()
    l = sb.bindings("mysql")
    assert len(l) == 2
    oracle_found = False
    mariadb_found = False
    for b in l:
        if b["provider"] == "oracle":
            oracle_found = True
            assert b["type"] == "mysql"
            assert b["username"] == "john"
            assert b["password"] == "L&ia6W@n7epi18a"
            assert b["url"] == "mysql://192.168.94.102:3306/school"

        if b["provider"] == "mariadb":
            mariadb_found = True
            assert b["type"] == "mysql"
            assert b["username"] == "jane"
            assert b["password"] == "o4%bGt#D8v2i0ja"
            assert b["uri"] == "mysql://192.168.94.103:7687/school"

    assert oracle_found and mariadb_found

    l = sb.bindings("mysql", "oracle")
    assert len(l) == 1
    b = l[0]
    assert b["type"] == "mysql"
    assert b["provider"] == "oracle"
    assert b["username"] == "john"
    assert b["password"] == "L&ia6W@n7epi18a"
    assert b["url"] == "mysql://192.168.94.102:3306/school"

    l = sb.bindings("mysql", "mariadb")
    assert len(l) == 1
    b = l[0]
    assert b["type"] == "mysql"
    assert b["provider"] == "mariadb"
    assert b["username"] == "jane"
    assert b["password"] == "o4%bGt#D8v2i0ja"
    assert b["uri"] == "mysql://192.168.94.103:7687/school"

def test_all_bindings(tmpdir, monkeypatch):
    bindings_dir = tmpdir.mkdir("bindings")
    junk = bindings_dir.join("junk")
    junk.write("junk text")
    sb1 = tmpdir.join("bindings").mkdir("sb1")
    sb1.mkdir("sub1")
    _type = sb1.join("type")
    _type.write("mysql")
    username = sb1.join("username")
    username.write("john")
    password = sb1.join("password")
    password.write("L&ia6W@n7epi18a")
    url = sb1.join("url")
    url.write("mysql://192.168.94.102:3306/school")

    sb2 = tmpdir.join("bindings").mkdir("sb2")
    _type = sb2.join("type")
    _type.write("neo4j")
    username = sb2.join("username")
    username.write("jane")
    password = sb2.join("password")
    password.write("o4%bGt#D8v2i0ja")
    uri = sb2.join("uri")
    uri.write("neo4j://192.168.94.103:7687/cr")

    monkeypatch.setenv("SERVICE_BINDING_ROOT", str(bindings_dir))

    sb = binding.ServiceBinding()
    l = sb.all_bindings()
    assert len(l) == 2
    mysql_found = False
    neo4j_found = False
    for b in l:
        if b["type"] == "mysql":
            mysql_found = True
            assert b["username"] == "john"
            assert b["password"] == "L&ia6W@n7epi18a"
            assert b["url"] == "mysql://192.168.94.102:3306/school"

        if b["type"] == "neo4j":
            neo4j_found = True
            assert b["username"] == "jane"
            assert b["password"] == "o4%bGt#D8v2i0ja"
            assert b["uri"] == "neo4j://192.168.94.103:7687/cr"

    assert mysql_found and neo4j_found


def test_missing_service_binding_root(tmpdir):
    sb1 = tmpdir.mkdir("bindings").mkdir("sb1")
    _type = sb1.join("type")
    _type.write("mysql")
    username = sb1.join("username")
    username.write("john")

    with pytest.raises(binding.ServiceBindingRootMissingError):
        sb = binding.ServiceBinding()

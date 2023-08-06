#!/usr/bin/bash

_args=("$@") # All parameters from terminal.

app_name='primaryschool'

update_gitignore(){
    git rm -r --cached . && git add .
    read -p "commit now?(y/N)" commit_now
    [[ "Yy" == *"${commit_now}"* ]] && git commit -m 'update .gitignore'
    echo "gitignore updated!"
}

_xgettext(){
    xgettext -v -j -L Python --output=$app_name/locale/$app_name.pot \
    $(find $app_name/ -name "*.py")

    for _po in $(find $app_name/locale/ -name "*.po"); do
        msgmerge -U -v $_po $app_name/locale/$app_name.pot
    done
}

_msgfmt(){
    for _po in $(find $app_name/locale -name "*.po"); do
        echo -e "$_po --> ${_po/.po/.mo}"
        msgfmt -v -o ${_po/.po/.mo} $_po
    done
}

p8(){
    isort $app_name/
    autopep8 -i -a -a -r -v $app_name/
    isort $app_name.py
    autopep8 -i -a -a -r -v $app_name.py
    isort ./setup.py
    autopep8 -i -a -a -r -v ./setup.py
}

git_add(){
    p8; git add .
}

_pip3(){
    python3 $app_name.py req_dev_u
}

twine_upload(){
    twine upload dist/*
}

bdist(){
    _msgfmt
    rm -rf dist/ build/ $app_name.egg-info/
    python3 setup.py sdist bdist_wheel
}

bdist_deb(){
    rm -rf deb_dist/  dist/  $app_name.egg-info/ $app_name*.tar.gz
    python3 setup.py --command-packages=stdeb.command bdist_deb
}

_i_test(){
    bdist
    pip3 uninstall $app_name -y
    pip3 install dist/*.whl
    $app_name
}


_start(){
    [[ -f "$app_name/locale/en_US/LC_MESSAGES/$app_name.mo" ]] || _msgfmt
    python3 $app_name.py st
}

active_venv(){
    [[ -f "./venv/bin/activate" ]] || \
    [[ -f $(which virtualenv) ]] && virtualenv venv || \
    echo "Installing virtualenv..." && pip3 install -U virtualenv
    source venv/bin/activate
}

cat_bt(){
    echo $app_name.sh; cat -bt $app_name.sh
    echo $app_name.py; cat -bt $app_name.py
    echo setup.py;  cat -bt setup.py
    for f in $(find $app_name/ -name "*.py" -o -name "*.po")
    do
        echo $f
        cat -bt $f
    done
}

test(){
    python3 $app_name.py test
}

tu(){       twine_upload;       }
ugi(){      update_gitignore;   }
tst(){      test;               }

gita(){     git_add;            }
bd(){       bdist;              }
kc(){       keep_code;          }

p3(){       active_venv;_pip3;  }
msgf(){     _msgfmt;            }
xget(){     _xgettext;          }

its(){       _i_test;           }
bdup(){     bd; tu;             }
_s(){       _start;             }

venv(){     active_venv;        }
_cat(){     cat_bt;             }
_cat_(){    _cat | tr -s '\n';  }

bdeb(){     bdist_deb;          }
wcl(){      _cat_ | wc -l;      }

${_args[0]}

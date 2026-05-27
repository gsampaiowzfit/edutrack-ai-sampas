import os
import importlib
import sys

def main():
    sys.path.insert(0, os.path.abspath('.'))
    test_files = [f[:-3] for f in os.listdir('workflow_tests') if f.startswith('test_') and f.endswith('.py')]
    
    passed = 0
    failed = 0
    
    for filename in test_files:
        print(f"\nRodando testes em: workflow_tests/{filename}.py")
        try:
            module = importlib.import_module(f"workflow_tests.{filename}")
            for attr_name in dir(module):
                if attr_name.startswith('test_'):
                    test_func = getattr(module, attr_name)
                    if callable(test_func):
                        try:
                            test_func()
                            print(f"  [PASS] {attr_name}")
                            passed += 1
                        except AssertionError as e:
                            print(f"  [FAIL] {attr_name}: {e}")
                            failed += 1
                        except Exception as e:
                            print(f"  [ERROR] {attr_name}: {e}")
                            failed += 1
        except Exception as e:
            print(f"Erro ao importar {filename}: {e}")
            failed += 1
            
    print(f"\nResultado final: {passed} passaram, {failed} falharam.")
    if failed > 0:
        sys.exit(1)

if __name__ == '__main__':
    main()

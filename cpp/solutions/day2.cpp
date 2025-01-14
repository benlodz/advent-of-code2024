#include <common/common.hpp>

int main(int argc, char argv[]) {
  auto logger = getLogger("test logger");
  logger->info("Test!");
  return 0;
}
